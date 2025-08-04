"""
Webhook Server Module
HTTP server to receive finish line signals for race timing.
"""

import json
import threading
from datetime import datetime
from typing import Optional, Callable, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class WebhookHandler(BaseHTTPRequestHandler):
    """HTTP request handler for webhook endpoints."""
    
    def __init__(self, *args, finish_callback=None, api_key=None, **kwargs):
        self.finish_callback = finish_callback
        self.api_key = api_key
        super().__init__(*args, **kwargs)
        
    def do_POST(self):
        """Handle POST requests for finish signals."""
        try:
            # Parse URL
            parsed_url = urlparse(self.path)
            
            # Check if this is the finish endpoint
            if parsed_url.path == "/finish":
                self.handle_finish_signal()
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
            
    def handle_finish_signal(self):
        """Handle finish signal webhook."""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read request body
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            # Validate API key if required
            if self.api_key:
                if not self.validate_api_key(data):
                    self.send_error(401, "Invalid API key")
                    return
                    
            # Extract finish data
            lane = data.get('lane', 1)
            participant_id = data.get('participant_id')
            finish_time = datetime.now()
            
            # Call the finish callback
            if self.finish_callback:
                self.finish_callback(finish_time, lane, participant_id)
                
            # Send success response
            response = {
                "status": "success",
                "message": "Finish signal received",
                "timestamp": finish_time.isoformat(),
                "lane": lane,
                "participant_id": participant_id
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON data")
        except Exception as e:
            self.send_error(500, f"Error processing finish signal: {str(e)}")
            
    def validate_api_key(self, data: Dict[str, Any]) -> bool:
        """Validate API key from request."""
        provided_key = data.get('api_key')
        if not provided_key:
            return False
            
        # Simple key validation (can be enhanced with HMAC)
        return provided_key == self.api_key
        
    def log_message(self, format, *args):
        """Override to reduce logging noise."""
        # Only log errors and important messages
        if "error" in format.lower() or "exception" in format.lower():
            super().log_message(format, *args)

class WebhookServer:
    """Webhook server for receiving finish line signals."""
    
    def __init__(self, port: int = 8080, api_key: Optional[str] = None):
        self.port = port
        self.api_key = api_key
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.finish_callback = None
        
    def set_finish_callback(self, callback: Callable[[datetime, int, Optional[str]], None]):
        """Set the callback function for finish signals."""
        self.finish_callback = callback
        
    def start_server(self):
        """Start the webhook server."""
        if self.is_running:
            return
            
        try:
            # Create custom handler class with callback
            handler_class = type('CustomHandler', (WebhookHandler,), {
                'finish_callback': self.finish_callback,
                'api_key': self.api_key
            })
            
            # Create server
            self.server = HTTPServer(('localhost', self.port), handler_class)
            
            # Start server in separate thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.is_running = True
            
        except Exception as e:
            pass  # Log error silently in production
            
    def stop_server(self):
        """Stop the webhook server."""
        if not self.is_running:
            return
            
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                
            if self.server_thread:
                self.server_thread.join(timeout=5)
                
            self.is_running = False
            
        except Exception as e:
            pass  # Log error silently in production
            
    def is_server_running(self) -> bool:
        """Check if the server is running."""
        return self.is_running
        
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        return {
            "is_running": self.is_running,
            "port": self.port,
            "endpoint": f"http://localhost:{self.port}/finish",
            "api_key_required": bool(self.api_key)
        }

 
#!/usr/bin/env python3
"""
Simple Health Monitor Server
This script creates a basic health monitor that runs on port 6767
"""

import http.server
import socketserver
import json
import time
from datetime import datetime

class HealthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            # Simple health check endpoint
            response = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'uptime': time.time()
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/':
            # Main page with health information
            response = {
                'message': 'Health Monitor Server',
                'status': 'healthy',
                'port': 6767,
                'timestamp': datetime.now().isoformat()
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        else:
            # Default 404
            self.send_response(404)
            self.end_headers()

def run_health_monitor(port=6767):
    """Run the health monitor server"""
    with socketserver.TCPServer(("", port), HealthHandler) as httpd:
        print(f"Health Monitor Server running on port {port}")
        print("Endpoints:")
        print("  GET /health - Health check endpoint")
        print("  GET / - Main page")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nHealth monitor server stopped.")

if __name__ == "__main__":
    run_health_monitor(6767)
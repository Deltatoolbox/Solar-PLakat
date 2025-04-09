import http.server
import socketserver

PORT = 8080
ADDRESS = "127.0.0.1"

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((ADDRESS, PORT), Handler) as httpd:
    print(f"Serving on http://{ADDRESS}:{PORT}")
    httpd.serve_forever()

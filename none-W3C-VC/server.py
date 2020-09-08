import http.server
import socketserver
from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("Request for:" + self.path)
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        if (self.path == '/secure/w3c-vc'):
            self.wfile.write(b'Hello w3c-vc')
        


httpd = socketserver.TCPServer(('', 8080), Handler)
httpd.serve_forever()
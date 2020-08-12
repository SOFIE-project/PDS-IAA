import http.server
import socketserver
from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("Request for:" + self.path)
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        if (self.path == '/secure/jwt'):
            self.wfile.write(b'Hello jwt')
        


httpd = socketserver.TCPServer(('', 8080), Handler)
httpd.serve_forever()
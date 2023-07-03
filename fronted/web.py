from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from backend.Agent import run2
from backend.AgentOneByOne import run1


def process_query(text, query_method):
    if query_method == 'run1':
        answer = run1(text)
    elif query_method == 'run2':
        answer = run2(text)
    else:
        answer = 'Invalid query method'

    return answer

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 解析请求的内容
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        text = params.get('text', [''])[0]
        query_method = params.get('queryMethod', ['run1'])[0]

        answer = process_query(text, query_method)

        response = {'answer': answer}
        json_response = json.dumps(response)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(json_response.encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self.path = '/front.html'

        try:
            with open(self.path[1:], 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')


def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server(8000)


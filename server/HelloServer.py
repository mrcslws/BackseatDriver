import time
import BaseHTTPServer

# Use this for live-streaming events from the client for online learning.
# I haven't consumed this yet.

HOST_NAME = ''
PORT_NUMBER = 8000

CONTENTS_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>BackseatDriver</title>
</head>
<body>
%s
</body>
</html>
"""

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(CONTENTS_TEMPLATE % ("<p>You accessed path: %s</p>" % self.path))
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        print time.asctime(), "Received POST - %s" % post_body
        self.send_response(200)
        self.end_headers()


if __name__ == '__main__':
    httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

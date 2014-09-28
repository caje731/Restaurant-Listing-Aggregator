import CGIHTTPServer, BaseHTTPServer
httpd = BaseHTTPServer.HTTPServer(('',8000),CGIHTTPServer.CGIHTTPRequestHandler)
httpd.serve_forever()

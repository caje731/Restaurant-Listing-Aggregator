import CGIHTTPServer, BaseHTTPServer
httpd = BaseHTTPServer.HTTPServer(('',8001),CGIHTTPServer.CGIHTTPRequestHandler)
httpd.serve_forever()

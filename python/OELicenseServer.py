#!/usr/bin/env python
#############################################################################
# Copyright (C) 2013 OpenEye Scientific Software, Inc.
#############################################################################
# This is a reference implementation provided for convenience. This software
# is not intended for production use because:
# 1) There is no encryption 
# 2) There is no logging
# 3) There are more industrial solutions available from Twisted Framework 
#    (http://twistedmatrix.com/).
#############################################################################

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import httplib
import subprocess
import sys, os
import threading
import shlex
import socket

class Handler(BaseHTTPRequestHandler):
    def getLicense(self):
        """Load the license from the file system on each request."""
        name = None
        if "OE_DIR" in os.environ:
            name = os.environ["OE_DIR"] + "/oe_license.txt"
        elif "OE_LICENSE" in os.environ:
            name = os.environ["OE_LICENSE"]
        elif os.path.exists("./oe_license.txt"):
            name = "./oe_license.txt"
        else:
            raise Exception("Could not find license in OE_DIR, OE_LICENSE or in the current directory.")
        
        content = None
        with open(name, "r") as fd:
           content = fd.read()
        return content    

    def do_GET(self):
        code = 200  # OEAddLicenseFromHttp() only recognizes response code 200
        try:
            content = self.getLicense() 
        except Exception, e:
            code = 500
            content = e.message
            
        self.send_response(code)
        self.send_header("Content-type", "text/plain")     # text/plain is a requirement
        self.send_header("Content-length", len(content))
        self.end_headers()
        self.wfile.write(content)
        self.wfile.write('\n')
        return

class ThreadedHTTPServer(HTTPServer, ThreadingMixIn):
    pass

if __name__ == '__main__':
    port = 8300  # change to match your needs
    httpd = ThreadedHTTPServer(('', port), Handler)
    print "Use http://%s:%d/ as the license server URL." % (socket.gethostname(), port)
    httpd.serve_forever()


#!/usr/bin/env python
# -*- coding: utf8 -*- 
# arguments: host port repo
#     host - host address to listen
#     port - port to listen
#     repo - package repository directory

__version__ = '0.1'

import json
import os
import os.path
import sys

from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


# directory structure of package repository:
# repo
# +-- com.example.hello
#     +-- label (text)
#     +-- version (text)
#     +-- icon (PNG image)
#     +-- package (APK archive)
# +-- ...
class AndroidPackageRequestHandler(SimpleHTTPRequestHandler):

    server_version = 'AndroidPackageServer/%s' % __version__
    
    def do_GET(self):
        # /count and /list are obsolete
        if self.path == '/count' or self.path == '/list':
            packages = os.listdir('.')
            if self.path == '/count':
                content = str(len(packages))
            else:
                content = '\n'.join(packages)
            content += '\n'
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/packages':
            favorites = file("../favorite").readlines()
            favorites = [f.rstrip() for f in favorites]
            names = os.listdir('.')
            packages = []
            for name in names:
                label = read_content(os.path.join(name, 'label'))
                version = read_content(os.path.join(name, 'version'))
                package_path = os.path.join(name, 'package')
                category = read_content(os.path.join(name,'category'))
                category_1  = read_content(os.path.join(name, 'category_1'))
                favorite = name in favorites
                try:
                    size = os.stat(package_path).st_size
                except OSError:
                    size = 0
                package = {
                    'name': name,
                    'category' : category,
                    'category_1' : category_1,
                    'label': label,
                    'version': version,
                    'size': size,
                    'favorite': favorite,
                }
                packages.append(package)
            content = json.dumps(packages)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/version':
            content = '1\n'
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            return SimpleHTTPRequestHandler.do_GET(self)


class AndroidPackageServer(ThreadingMixIn, HTTPServer):

    def __init__(self, address):
        HTTPServer.__init__(self, address, AndroidPackageRequestHandler)


def read_content(path):
    try:
        content = open(path).read().strip()
    except IOError:
        content = ''
    return content

def main(argv):
    host = argv[1] if len(argv) > 1 else ''
    port = int(argv[2]) if len(argv) > 2 else 8080
    home = argv[3] if len(argv) > 3 else 'repo/'
    os.chdir(home)
    address = (host, port)
    server = AndroidPackageServer(address)
    server.serve_forever()


if __name__ == '__main__':
    sys.exit(main(sys.argv))

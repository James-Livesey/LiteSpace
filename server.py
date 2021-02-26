import http.server
import socketserver
import json
import os

import actions

serverConfig = json.load(open(os.path.join("config", "server.json"), "r"))
routes = json.load(open(os.path.join("config", "routes.json"), "r"))
mimetypes = json.load(open(os.path.join("config", "mimetypes.json"), "r"))

class Handler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]

        if path.startswith("/"):
            path = path[1:]

        resolvedResponse = actions.actionRouter.resolve(routes["routes"], path, routes["default"])

        self.send_response(resolvedResponse.status)
        self.send_header("Content-type", mimetypes[resolvedResponse.extension])
        self.end_headers()
        self.wfile.write(resolvedResponse.data)

socketserver.TCPServer.allow_reuse_address = True
httpSocket = socketserver.TCPServer((serverConfig["address"], serverConfig["port"]), Handler)

print("Serving on {address}:{port}".format(address = serverConfig["address"], port = serverConfig["port"]))

try:
    httpSocket.serve_forever()
except:
    httpSocket.shutdown()
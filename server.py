from http.server  import HTTPServer, BaseHTTPRequestHandler
from json         import loads, dumps
from json.decoder import JSONDecodeError

class Command():
    def __init__(self):
        pass

    def execute(self, drone):
        pass

class DistanceCommand(Command):
    def __init__(self, dx, dy, dz):
        Command.__init__(self)
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def execute(self, drone):
        drone.setRelativeTarget(self.dx, self.dy, self.dz)

class StopCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def execute(self, drone):
        drone.stopRotors()


class CrazyHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        request        = self.rfile.read(content_length)

        try:
            json = loads(request.decode())

            if "command" in json:
                if json["command"] == "stop":
                    self.server.commandQueue.put(StopCommand())

                else:
                    raise Exception("Invalid command: {}".format(json["command"]))

            elif "distance" in json:
                [ dx, dy, dz ] = json["distance"]
                self.server.commandQueue.put(DistanceCommand(dx, dy, dz))

            else:
                raise Exception("Unexpected input: {}".format(json))

            reply = { "ok" : json }
        except Exception as e:
           reply = { "error" : str(e) }

        self._set_headers()
        self.wfile.write(dumps(reply).encode())


def runServer(hostname, port, commandQueue):
    server              = HTTPServer((hostname, port), CrazyHandler)
    server.commandQueue = commandQueue
    server.serve_forever()

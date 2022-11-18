"""Application main module running an async HTTP web server."""

import argparse
from aiohttp.web import Application, run_app, post
from handler.handler import handle_optimize_request

parser = argparse.ArgumentParser()
parser.add_argument('--port', type = int, nargs = '?', default = 8888)

args = parser.parse_args()
server_port = args.port

app = Application()
app.add_routes([post('/spaceship/optimize', handle_optimize_request)])

if __name__ == '__main__':
    run_app(app, port = server_port)

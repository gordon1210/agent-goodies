"""Local-only example server; --three-root selects an existing Three.js package."""
import argparse
import functools
import http.server
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--three-root', type=Path)
parser.add_argument('--port', type=int, default=8765)
args = parser.parse_args()
three = args.three_root.resolve() if args.three_root else None

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        from urllib.parse import unquote, urlsplit
        relative = unquote(urlsplit(path).path).lstrip('/')
        base = ROOT
        if relative.startswith('vendor/'):
            if three is None:
                return str(ROOT / 'unavailable-vendor')
            base, relative = three, relative.removeprefix('vendor/')
        target = (base / relative).resolve()
        if not target.is_relative_to(base):
            return str(ROOT / 'unavailable-path')
        return str(target)

http.server.ThreadingHTTPServer(('127.0.0.1', args.port), functools.partial(Handler, directory=str(ROOT))).serve_forever()

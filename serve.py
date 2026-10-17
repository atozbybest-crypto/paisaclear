#!/usr/bin/env python3
"""Local preview server for the multi-page build.

    python serve.py                 start, pick a free port, open the browser
    python serve.py --no-open       just serve (useful in scripts)
    python serve.py --port 9000     try a specific port first

Ctrl+C stops it. Standard library only.
"""

from __future__ import annotations

import argparse
import http.server
import socket
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
CANDIDATE_PORTS = [8742, 8743, 8744, 8750, 8760, 8080, 8000]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def end_headers(self):
        # Always show the latest build while editing locally.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):  # keep the console readable
        pass


def free_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the PaisaClear build locally.")
    parser.add_argument("--port", type=int, help="port to try first")
    parser.add_argument("--no-open", action="store_true", help="do not open a browser")
    args = parser.parse_args()

    if not SITE.exists():
        print("site/ is missing. Run `python build.py` first.", file=sys.stderr)
        return 1

    order = ([args.port] if args.port else []) + CANDIDATE_PORTS
    port = next((p for p in order if free_port(p)), None)
    if port is None:
        print("No free port found in " + ", ".join(map(str, order)), file=sys.stderr)
        return 1

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"

    print()
    print("  PaisaClear is running")
    print("  " + url)
    print()
    print("  Press Ctrl+C to stop.")
    print()

    if not args.no_open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

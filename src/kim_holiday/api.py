"""Small JSON HTTP API for approval-gated content drafts."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .pipeline import ContentDraftPipeline, DraftRejected


class DraftAPIHandler(BaseHTTPRequestHandler):
    pipeline = ContentDraftPipeline()

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
        else:
            self._send_json(404, {"error": "not_found", "message": "Route not found."})

    def do_POST(self) -> None:
        if self.path != "/draft":
            self._send_json(404, {"error": "not_found", "message": "Route not found."})
            return
        try:
            length = int(self.headers.get("Content-Length", ""))
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "invalid_json", "message": "Request body must be valid JSON."})
            return
        if not isinstance(payload, dict) or not isinstance(payload.get("topic"), str):
            self._send_json(400, {"error": "invalid_request", "message": "JSON object with a string topic is required."})
            return
        try:
            draft = self.pipeline.run(payload["topic"])
        except DraftRejected as exc:
            self._send_json(422, {"error": "draft_rejected", "message": str(exc)})
            return
        self._send_json(200, draft)

    def do_PUT(self) -> None:
        self._send_json(405, {"error": "method_not_allowed", "message": "Use POST /draft."})

    def do_DELETE(self) -> None:
        self._send_json(405, {"error": "method_not_allowed", "message": "Use POST /draft."})

    def log_message(self, format: str, *args: Any) -> None:
        return


def serve(host: str = "0.0.0.0", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), DraftAPIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Kim Holiday draft API.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    serve(args.host, args.port)


if __name__ == "__main__":
    main()

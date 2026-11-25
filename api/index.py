import json
import sys
import traceback
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from app.main import app
except BaseException as exc:
    _startup_error = str(exc)
    _startup_trace = traceback.format_exc().splitlines()

    async def app(scope, receive, send):
        if scope["type"] == "http":
            body = json.dumps(
                {
                    "error": "Startup failed",
                    "detail": _startup_error,
                    "traceback": _startup_trace,
                },
                indent=2,
            ).encode("utf-8")
            await send(
                {
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [(b"content-type", b"application/json")],
                }
            )
            await send({"type": "http.response.body", "body": body})

import sys
import traceback
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from app.main import app
except Exception as exc:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    _startup_error = str(exc)
    _startup_trace = traceback.format_exc()
    app = FastAPI()

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
    async def startup_error_handler(full_path: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Startup failed",
                "detail": _startup_error,
                "traceback": _startup_trace.splitlines(),
            },
        )

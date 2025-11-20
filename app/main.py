from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

from app.verifier import run_verification

app = FastAPI(title="LinkedIn Cookie Verifier")


class CookiePayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    li_at: str
    jsessionid: str | None = ""


@app.post("/verify")
async def verify_cookies(payload: CookiePayload):
    """Verify LinkedIn cookies using Playwright-backed logic."""
    try:
        result = await run_verification(payload.li_at, payload.jsessionid or "")
        return {
            "status": result.status.value,
            "username": result.username,
            "full_name": result.full_name,
            "profile_url": result.profile_url,
            "error_message": result.error_message,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
async def health():
    """Simple readiness probe."""
    return {"status": "ok"}

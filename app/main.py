from typing import Optional

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, ConfigDict

from app.verifier import run_verification
from app.services.linkedin_cookie_verifier import warm_playwright

app = FastAPI(title="LinkedIn Cookie Verifier")


class CookiePayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    li_at: str
    jsessionid: Optional[str] = ""


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

@app.on_event("startup")
async def startup_event():
    """Prime Playwright browsers if Playwright mode is enabled."""
    await warm_playwright()


@app.get("/")
async def root():
    """Landing endpoint with usage guidance."""
    return {"status": "ok", "message": "POST /verify with li_at and optional jsessionid"}


@app.get("/verify")
async def verify_cookies_get():
    """Explicit guidance for clients accidentally using GET."""
    raise HTTPException(
        status_code=405,
        detail="Use POST /verify with JSON body {\"li_at\": \"...\", \"jsessionid\": \"\"}",
    )


@app.get("/favicon.ico")
async def favicon():
    """Silence favicon lookups in logs."""
    return Response(status_code=204)

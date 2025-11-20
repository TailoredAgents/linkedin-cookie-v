LinkedIn Cookie Verifier microservice
====================================

FastAPI service that wraps the existing `services.linkedin_cookie_verifier.verify_linkedin_cookies` Playwright logic. It accepts LinkedIn cookies, runs the Playwright-based verification, and returns the status/unpacked profile data as JSON. Designed to run as a standalone Render service the main API can call.

Endpoints
---------
- `POST /verify` — body `{"li_at": "...", "jsessionid": ""}`; returns `status`, `username`, `full_name`, `profile_url`, `error_message`.
- `GET /health` — returns `{"status": "ok"}` for Render health checks.

Local setup
-----------
1. Python 3.11 recommended (`runtime.txt` set to 3.11.9).
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `bash scripts/install_playwright.sh` (downloads Chromium to `PLAYWRIGHT_BROWSERS_PATH`, default `/tmp/playwright`)
5. `uvicorn app.main:app --host 0.0.0.0 --port 8000`

Environment
-----------
- `LINKEDIN_VERIFIER_MODE=playwright` (set in this service)
- `PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright` (keeps browser download writable on Render)
- `PYTHONUNBUFFERED=1`
- Optional fallback settings: `LINKEDIN_COOKIE_VERIFIER_API`, `LINKEDIN_COOKIE_VERIFIER_API_KEY`, `LINKEDIN_COOKIE_VERIFIER_API_HEADER`.

Render deployment
-----------------
- Service type: Web Service, Runtime: Python 3.11
- Build command:
  ```
  pip install -r requirements.txt
  bash scripts/install_playwright.sh
  ```
- Start command:
  ```
  uvicorn app.main:app --host=0.0.0.0 --port=$PORT
  ```
- Health check path: `/health`

Main API configuration
----------------------
Point the primary API at this service:
- `LINKEDIN_VERIFIER_MODE=api`
- `LINKEDIN_COOKIE_VERIFIER_API=https://<your-render-service>/verify`
- Include optional auth header/key if you add it in `app/main.py`.

Usage example
-------------
```
curl -X POST http://localhost:8000/verify \
  -H 'Content-Type: application/json' \
  -d '{"li_at":"<li_at_cookie>", "jsessionid":""}'
```

Notes
-----
- The Playwright verifier is vendored from the main codebase under `app/services/linkedin_cookie_verifier.py`. An extremely light audit logger stub lives at `app/services/audit_logging_service.py`.
- For inter-service auth, add header checks in `app/main.py` and propagate the expected header/value via environment variables.

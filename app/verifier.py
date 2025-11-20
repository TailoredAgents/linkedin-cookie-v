"""Thin wrapper around the LinkedIn cookie verifier."""

from app.services.linkedin_cookie_verifier import verify_linkedin_cookies


async def run_verification(li_at: str, jsessionid: str = ""):
    """Run verification with stable tenant/user identifiers for audit logs."""
    return await verify_linkedin_cookies(
        li_at=li_at,
        jsessionid=jsessionid or "",
        tenant_id="external",
        user_id=0,
    )


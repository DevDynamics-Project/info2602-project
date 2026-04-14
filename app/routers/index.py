from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies.auth import IsUserLoggedIn
from . import router, templates


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, is_logged_in: IsUserLoggedIn):
    if is_logged_in:
        return RedirectResponse(url="/app")
    return RedirectResponse(url="/login")

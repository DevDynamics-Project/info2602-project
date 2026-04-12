from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
import jwt
from jwt.exceptions import InvalidTokenError
from app.config import get_settings
from app.models.user import User
from app.dependencies.session import SessionDep
from app.repositories.user import UserRepository

# async def get_current_user(request: Request, db:SessionDep):

#     # ✅ READ COOKIE INSTEAD OF HEADER
#     token = request.cookies.get("access_token")

#     if not token:
#         raise HTTPException(status_code=401, detail="No token found")

#     # ⚠️ TEMP DEBUG (you can remove later)
#     print("TOKEN:", token)

#     # If you're NOT using JWT, just return user directly:
#     user = token   # or fetch from DB if needed

#     return user
async def get_current_user(request: Request, db: SessionDep):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No token found")

    try:
        payload = jwt.decode(
            token,
            get_settings().secret_key,
            algorithms=[get_settings().jwt_algorithm]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.get(User, int(user_id))

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    #=======================================================================

async def is_logged_in(request: Request, db:SessionDep):
    try:
        await get_current_user(request, db)
        return True
    except Exception:
        return False

IsUserLoggedIn = Annotated[bool, Depends(is_logged_in)]
AuthDep = Annotated[User, Depends(get_current_user)]

async def is_admin(user: User):
    return user.role == "admin"

async def is_admin_dep(user: AuthDep):
    if not await is_admin(user):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to access this page",
            )
    return user

AdminDep = Annotated[User, Depends(is_admin_dep)]

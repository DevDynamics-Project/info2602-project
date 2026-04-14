from app.repositories.user import UserRepository
from app.models.user import UserBase
from app.utilities.security import encrypt_password, verify_password, create_access_token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, email: str, password: str):
        hashed = encrypt_password(password)
        user_data = UserBase(username=username, email=email, password=hashed)
        return self.user_repo.create(user_data)

    def authenticate_user(self, username: str, password: str) -> str | None:
        user = self.user_repo.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return create_access_token({"sub": str(user.id)})

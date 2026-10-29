from datetime import datetime, timezone, timedelta
import jwt
from pwdlib import PasswordHash
from src.config import settings


class Security:
    def __init__(self):
        self.settings = settings
        self.password_hash = PasswordHash.recommended()

    def get_password_hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hash.verify(password, hashed_password)

    def create_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode |= {"exp":expire}

        return jwt.encode(
            to_encode,
            self.settings.SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )

    def decode_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

security = Security()
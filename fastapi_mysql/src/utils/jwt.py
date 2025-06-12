from datetime import datetime, timedelta, UTC
from typing import Any, Dict
from fastapi import HTTPException, status
from jose import JWTError, jwt
from configs import get_settings


class JWT:
    def __init__(self):
        settings = get_settings()
        jwt_config = settings.jwt

        self.algorithm: str = jwt_config.jwt_algorithm
        self.secret: str = jwt_config.jwt_secret_key
        self.access_token_expire_min: int = jwt_config.access_token_expires_in
        self.refresh_token_expire_in: int = jwt_config.refresh_token_expires_in

    def create_access_token(self, payload: Dict[str, Any]) -> str:
        try:
            payload = payload.copy()
            payload["exp"] = datetime.now(UTC) + timedelta(
                minutes=self.access_token_expire_min
            )

            return jwt.encode(payload, self.secret, algorithm=self.algorithm)

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"JWT encoding failed: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {repr(e)}",
            )

    def create_refresh_token(self, payload: Dict[str, Any]) -> str:
        try:
            payload = payload.copy()
            payload.update(
                {
                    "exp": datetime.now(UTC)
                    + timedelta(days=self.refresh_token_expire_in),
                    "type": "refresh_token",
                }
            )

            return jwt.encode(payload, self.secret, algorithm=self.algorithm)

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"JWT refresh encoding failed: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {repr(e)}",
            )

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Token decoding failed: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {repr(e)}",
            )

    def decode_refresh_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = self.decode_token(token)
            if payload.get("type") != "refresh_token":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type: expected refresh_token",
                )
            return payload
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {repr(e)}",
            )

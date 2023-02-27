import logging
from http import HTTPStatus
from typing import List
from uuid import UUID

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import settings
from core.core_model import CoreModel

logger = logging.getLogger(__name__)

JWT_SECRET = settings.JWT_SECRET_KEY
MOCK_TOKEN = settings.MOCK_AUTH_TOKEN
JWT_ALGORITHM = "HS256"


class AccessTokenPayload(CoreModel):
    """Access token payload"""

    fresh: bool
    iat: int
    jti: UUID
    type: str
    sub: UUID
    nbf: int
    exp: int
    name: str
    roles: List[str]
    device_id: str


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessTokenPayload:
        if MOCK_TOKEN:
            return get_mock_token()

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid authorization code.")

        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid authentication scheme.")

        try:
            decoded_token = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.PyJWTError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token or expired token.")

        logger.debug("jwt-token payload: %s", decoded_token)
        token = AccessTokenPayload(**decoded_token)
        return token


def get_mock_token():
    """test only token. For run without real token"""
    return AccessTokenPayload(
        fresh=False,
        iat=1675081706,
        jti="00000000-0000-0000-0000-000000000000",
        type="access",
        sub="00000000-0000-0000-0000-000000000000",
        nbf=1675081706,
        exp=1675085306,
        name="mock_user",
        roles=["MOCK_USER"],
        device_id="Mock device",
    )


jwt_bearer = JWTBearer()

from datetime import UTC, datetime, timedelta
from typing import NamedTuple

from jwt import JWT, AbstractJWKBase, jwk_from_pem
from jwt.utils import get_int_from_datetime


class PrivatePublickPem(NamedTuple):
    private_pem: AbstractJWKBase
    public_pem: AbstractJWKBase


class AuthJWTCertService:
    def __init__(self) -> None:
        self._jwt = JWT()
        self.pems: PrivatePublickPem = self.load_pems()

    def load_pems(self) -> PrivatePublickPem:
        with open("public.pem", "rb") as f:
            public_pem = jwk_from_pem(f.read())

        with open("private.pem", "rb") as f:
            private_pem = jwk_from_pem(f.read())

        return PrivatePublickPem(private_pem=private_pem, public_pem=public_pem)

    def encode_jwt(
        self,
        user_id: int,
        role: str,
        exp_delta: timedelta,
    ) -> str:
        """
        encode jwt
        """
        payload = {
            "iat": get_int_from_datetime(datetime.now(UTC)),
            "exp": get_int_from_datetime(datetime.now(UTC) + exp_delta),
            "sub": "web",
            "lang": "RU",
            "u": user_id,
            "r": role,
        }

        return self._jwt.encode(payload=payload, key=self.pems.private_pem, alg="RS256")

    def decode_jwt(self, token: str) -> dict:
        return self._jwt.decode(
            message=token, key=self.pems.public_pem, algorithms={"RS256"}
        )


auth_jwt_service = AuthJWTCertService()

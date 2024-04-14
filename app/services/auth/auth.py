from datetime import UTC, datetime, timedelta
from functools import cached_property
from typing import NamedTuple

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt import JWT, AbstractJWKBase, jwk_from_pem
from jwt.utils import get_int_from_datetime


class PrivatePublickPem(NamedTuple):
    private_pem: AbstractJWKBase
    public_pem: AbstractJWKBase


class AuthJWTCertService:
    def __init__(self) -> None:
        self._jwt = JWT()
        self.pems: PrivatePublickPem

    @cached_property
    def get_public_pem(self) -> AbstractJWKBase:
        with open("public_key.pem", "rb") as f:
            pem = f.read()
            return jwk_from_pem(pem)

    def generate_pems(self) -> PrivatePublickPem:
        """
        generate private and publick pem for jwt
        """
        # Генерация приватного ключа
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Получение публичного ключа
        public_key = private_key.public_key()

        private_pem = (
            private_key.private_bytes(  # Сериализация и сохранение приватного ключа
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

        public_pem = (
            public_key.public_bytes(  # Сериализация и сохранение публичного ключа
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

        pems = PrivatePublickPem(
            private_pem=jwk_from_pem(private_pem), public_pem=jwk_from_pem(public_pem)
        )
        self.pems = pems

        with open("public_key.pem", "wb") as f:
            f.write(public_pem)

        return self.pems

    def encode_jwt(
        self,
        user_id: int,
        role: str,
        private_pem: AbstractJWKBase,
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

        return self._jwt.encode(payload=payload, key=private_pem, alg="RS256")

    def decode_jwt(self, token: str, public_pem: AbstractJWKBase) -> dict:
        return self._jwt.decode(message=token, key=public_pem, algorithms={"RS256"})


auth_service = AuthJWTCertService()

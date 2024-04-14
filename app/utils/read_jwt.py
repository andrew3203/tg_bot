from datetime import timedelta

from app.auth.services import AuthJWTCertService
from config.constants import Stage

auth_test_service = AuthJWTCertService(stage=Stage.TESTING)
auth_test_service.generate_pems()


def generate_sync_jwt(role: str, tariffs: list[dict], user_id: int):
    access = {"a": 1, "b": 1, "ccc": 1, role: 1}

    return auth_test_service.encode_jwt(
        user_id=user_id,
        access=access,
        tariffs=tariffs,
        private_pem=auth_test_service.pems.private_pem,
        exp_delta=timedelta(seconds=60),
    )

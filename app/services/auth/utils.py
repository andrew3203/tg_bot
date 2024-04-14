from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.fernet import Fernet


def generate_jwt_pems() -> None:
    """
    generate private and publick pem for jwt
    """
    # Генерация приватного ключа
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
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

    public_pem = public_key.public_bytes(  # Сериализация и сохранение публичного ключа
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open("public.pem", "wb") as f:
        f.write(public_pem)

    with open("private.pem", "wb") as f:
        f.write(private_pem)


def generate_password_key() -> None:
    """
    generate password_key
    """
    # Генерация приватного ключа
    password_hasher = Fernet.generate_key()

    with open("password_hasher.key", "wb") as f:
        f.write(password_hasher)

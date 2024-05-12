import logging
import uuid

from boto3 import Session
from botocore.client import BaseClient
from fastapi import UploadFile

from config.settings import settings
from app.utils.exceptions import CoreException, DataExeption

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self):
        self._aws_access_key_id = settings.S3_KEY_ID
        self._aws_secret_access_key = settings.S3_KEY
        self._aws_bucket = settings.S3_BUCKET
        self._aws_domain = settings.S3_DOMAIN
        self._region_name = settings.S3_REGION_NAME
        self._service_name = "s3"
        self._path = "messages"

    def _get_file_url(self, file_path: str) -> str:
        return f"https://{self._aws_bucket}.{self._aws_domain}/{file_path}"

    def _get_file_path(self, file_full_name: str) -> str:
        extension = file_full_name.split(".")[-1].lower()
        return f"{self._path}/{str(uuid.uuid4())}.{extension}"

    def upload(self, file: UploadFile) -> str:
        if file.filename is None:
            raise DataExeption(msg="Пустое название файла не допустимо")

        file_path = self._get_file_path(file.filename)

        try:
            session = Session(
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key,
                region_name=self._region_name,
            )
            client: BaseClient = session.client(
                service_name=self._service_name,
                endpoint_url=f"https://{self._aws_domain}",
            )
            client.upload_fileobj(
                file.file,
                settings.S3_BUCKET,
                file_path,
                ExtraArgs={"ContentType": file.content_type, "ACL": "public-read"},
            )
            client.close()
        except Exception as e:
            logger.error(f"Error upload file {str(e)}")
            raise CoreException(
                msg=f"Не получилось загрузить файл в хронилище: {str(e)}"
            )

        return self._get_file_url(file_path=file_path)

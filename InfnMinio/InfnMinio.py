from typing import Dict, Any
from pathlib import Path
import os

import requests, xmltodict
from minio import Minio


class InfnMinio(Minio):
    """
    A thin wrapper around Minio SDK to ease configuration on setups where STS-Wire is running.

    Example
    ```python
    from InfnMinio import InfnMinio as Minio
    minio = Minio.from_token(token="/path/to/your/.token", endpoint="minio.cloud.infn.it")
    minio.list_buckets()
    ```
    """
    @staticmethod
    def from_token(
        token: Path = None,
        endpoint: str = "minio.cloud.infn.it",
    ):
        """
        Creates a Minio Client instance from a token stored in the filesystem.
        """
        if token is None:
            home = os.environ.get("HOME")
            token = Path(home) / ".token"
        
        creds = InfnMinio.get_credentials(endpoint, token)

        return Minio(endpoint, **creds, secure=True)


    
    @staticmethod
    def get_credentials(endpoint: str, token: str) -> Dict[str, Any]:
        """
        Retrieve the credentials through the AssumeRoleWithWebIdentity endpoint
        """
        response = requests.post(f"https://{endpoint}", data=dict(
            Action="AssumeRoleWithWebIdentity",
            WebIdentityToken=open(token).read(),
            Version="2011-06-15",
            DurationSeconds=86400,
        ))

        response.raise_for_status()
        creds = (
            xmltodict
            .parse(response.text)
            .get('AssumeRoleWithWebIdentityResponse', {})
            .get('AssumeRoleWithWebIdentityResult', {})
            .get('Credentials', {})
        )

        return dict(
            access_key=creds.get('AccessKeyId', ""),
            secret_key=creds.get('SecretAccessKey', ""),
            session_token=creds.get('SessionToken', ""),
        )

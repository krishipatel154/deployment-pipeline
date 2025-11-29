# utils/s3.py
import os
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile

# Load from GitHub Secrets (already set)
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET")


async def upload_to_s3(file: UploadFile) -> str:
    """Upload file to S3 and return signed URL (valid 7 days)"""
    if not BUCKET_NAME:
        raise RuntimeError("S3_BUCKET not configured")

    key = f"profiles/{file.filename}"

    try:
        await file.seek(0)
        s3_client.upload_fileobj(
            file.file,
            BUCKET_NAME,
            key,
            ExtraArgs={
                "ContentType": file.content_type or "application/octet-stream",
            },
        )

        # Generate signed URL valid for 7 days
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=7 * 24 * 3600,  # 7 days
        )
        return url

    except ClientError as e:
        raise RuntimeError(f"S3 upload failed: {e}")
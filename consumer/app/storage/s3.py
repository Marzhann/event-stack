import boto3
from botocore.exceptions import ClientError


MAX_INLINE_BYTES = 64 * 1024  # 64KB


def get_s3_client(
        endpoint_url: str,
        access_key: str,
        secret_key: str
):
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="us-east-1"
    )

def ensure_bucket(s3, bucket: str):
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        # MinIO often returns 404/NoSuchBucket for missing
        if code in ("404", "NoSuchBucket", "NotFound"):
            s3.create_bucket(Bucket=bucket)
        else:
            raise

def put_object(s3, bucket: str, key: str, data:bytes, content_type: str = "application/octet-stream"):
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=data,
        ContentType=content_type
    )

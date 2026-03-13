import boto3
import os
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()

MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "password")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ROOT_USER,
    aws_secret_access_key=MINIO_ROOT_PASSWORD,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",  # Dummy region for MinIO
)

BUCKET_NAME = "resumes"

def ensure_bucket_exists():
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
    except:
        s3.create_bucket(Bucket=BUCKET_NAME)

def upload_file(file_content, object_name):
    ensure_bucket_exists()
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=object_name,
        Body=file_content,
        ContentType="application/pdf"
    )
    return f"{BUCKET_NAME}/{object_name}"

def download_file(object_name, download_path):
    ensure_bucket_exists()
    s3.download_file(BUCKET_NAME, object_name, download_path)
    return download_path

def clear_storage():
    """Remove all objects from the resumes bucket."""
    ensure_bucket_exists()
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    if 'Contents' in response:
        for obj in response['Contents']:
            s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
    print(f"Bucket {BUCKET_NAME} cleared.")

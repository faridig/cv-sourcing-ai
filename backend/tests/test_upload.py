import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.storage import s3, BUCKET_NAME
import io

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_minio():
    """Cleanup the resumes bucket after each test."""
    yield
    try:
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
    except Exception as e:
        print(f"Cleanup failed: {e}")

def test_upload_pdf_success():
    # Simulate a PDF file
    file_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    file_name = "test_cv.pdf"
    
    response = client.post(
        "/api/cv/upload",
        files={"file": (file_name, file_content, "application/pdf")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["filename"] == file_name
    assert "path" in data
    assert data["path"].startswith("resumes/")
    assert data["path"].endswith(".pdf")
    
    # Verify file is in MinIO
    object_key = data["path"].split("/")[-1]
    s3_obj = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
    assert s3_obj["Body"].read() == file_content

def test_upload_non_pdf_rejection():
    # Simulate a text file
    file_content = b"This is not a PDF."
    file_name = "test.txt"
    
    response = client.post(
        "/api/cv/upload",
        files={"file": (file_name, file_content, "text/plain")}
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Seuls les fichiers PDF sont acceptés."}

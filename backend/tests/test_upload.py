import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

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

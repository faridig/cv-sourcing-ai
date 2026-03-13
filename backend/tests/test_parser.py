import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.main import app

client = TestClient(app)

@patch("backend.app.main.download_file")
@patch("backend.app.main.parse_pdf")
def test_parse_cv_success(mock_parse, mock_download):
    # Mock des dépendances
    mock_download.return_value = "/tmp/fake.pdf"
    mock_parse.return_value = "# CV de Test\n\n## Expérience\n- Développeur Python"
    
    file_id = "test-uuid"
    response = client.post(f"/api/cv/parse/{file_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == file_id
    assert data["format"] == "markdown"
    assert "Développeur Python" in data["content"]
    
    mock_download.assert_called_once()
    mock_parse.assert_called_once()

@patch("backend.app.main.download_file")
def test_parse_cv_not_found(mock_download):
    # Simuler une erreur MinIO (NoSuchKey)
    mock_download.side_effect = Exception("NoSuchKey: The specified key does not exist.")
    
    file_id = "non-existent-id"
    response = client.post(f"/api/cv/parse/{file_id}")
    
    assert response.status_code == 404
    assert "Fichier non trouvé" in response.json()["detail"]

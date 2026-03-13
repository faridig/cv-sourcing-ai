import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from app.main import app

client = TestClient(app)

@patch("app.main.download_file")
@patch("app.main.parse_pdf")
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

@patch("app.main.download_file")
def test_parse_cv_not_found(mock_download):
    # Simuler une erreur MinIO réaliste (404 via ClientError)
    error_response = {'Error': {'Code': '404', 'Message': 'Not Found'}}
    mock_download.side_effect = ClientError(error_response, 'HeadObject')
    
    file_id = "non-existent-id"
    response = client.post(f"/api/cv/parse/{file_id}")
    
    assert response.status_code == 404
    assert "Fichier non trouvé" in response.json()["detail"]

@patch("app.main.download_file")
def test_parse_cv_storage_error(mock_download):
    # Simuler une autre erreur MinIO (500 via ClientError)
    error_response = {'Error': {'Code': '500', 'Message': 'Internal Server Error'}}
    mock_download.side_effect = ClientError(error_response, 'HeadObject')
    
    file_id = "error-id"
    response = client.post(f"/api/cv/parse/{file_id}")
    
    assert response.status_code == 500
    assert "Erreur lors de la communication" in response.json()["detail"]

@patch("app.main.download_file")
@patch("app.main.parse_pdf")
def test_parse_cv_internal_error(mock_parse, mock_download):
    # Simuler une erreur inattendue lors du parsing
    mock_download.return_value = "/tmp/fake.pdf"
    mock_parse.side_effect = Exception("Crash inattendu")
    
    file_id = "crash-id"
    response = client.post(f"/api/cv/parse/{file_id}")
    
    assert response.status_code == 500
    assert "Une erreur interne est survenue" in response.json()["detail"]
    assert "Crash inattendu" not in response.json()["detail"]  # Pas de fuite d'info

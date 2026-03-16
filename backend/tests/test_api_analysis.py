import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models import AnalyseCV, DynamiqueCarriere, CompetencesDouces, StackMetier, AuditRigueur

client = TestClient(app)

@pytest.fixture
def mock_analysis_data():
    return AnalyseCV(
        dynamique_carriere=DynamiqueCarriere(
            seniorite="Senior", 
            progression="Good",
            exposition_strategique="High"
        ),
        fit_culturel="Agile",
        rayonnement="None",
        langues=["English"],
        competences_douces=CompetencesDouces(
            leadership="Preuve leadership", 
            autonomie="Preuve autonomie", 
            travail_equipe="Preuve équipe", 
            communication="Preuve communication"
        ),
        stack_metier=StackMetier(principale=["Python"], secondaire=[], veille_et_normes=[]),
        mobilite="Paris",
        signaux_faibles="None",
        localisation="Paris, 75000",
        resume="A test CV",
        audit_rigueur=AuditRigueur(
            score_orthographe="Good",
            coherence_competences="High",
            coquilles_detectees=[]
        )
    )

@patch("app.main.download_file")
@patch("app.main.parse_pdf")
@patch("app.main.analyzer")
def test_analyze_cv_endpoint(mock_analyzer, mock_parse, mock_download, mock_analysis_data):
    # Setup mocks
    mock_parse.return_value = "This is the extracted text."
    mock_analyzer.analyze_cv.return_value = (mock_analysis_data, "# Augmented Dossier")
    
    # Execute
    response = client.post("/api/cv/analyze/test-uuid")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-uuid"
    assert data["analysis"]["dynamique_carriere"]["seniorite"] == "Senior"
    assert data["dossier_markdown"] == "# Augmented Dossier"
    assert "dossier_path" in data
    assert data["dossier_path"].endswith("test-uuid.md")
    
    mock_download.assert_called_once()
    mock_parse.assert_called_once()
    mock_analyzer.analyze_cv.assert_called_once_with("This is the extracted text.")

@patch("app.main.analyzer", None)
def test_analyze_cv_no_analyzer():
    response = client.post("/api/cv/analyze/test-uuid")
    assert response.status_code == 503
    assert "Service d'analyse IA non configuré" in response.json()["detail"]

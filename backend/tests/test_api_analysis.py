import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models import CVAnalysis, CareerDynamics, SoftSkills, TechStack

client = TestClient(app)

@pytest.fixture
def mock_analysis_data():
    return CVAnalysis(
        career_dynamics=CareerDynamics(seniority="Senior", progression="Good"),
        culture_fit="Agile",
        outreach="None",
        languages=["English"],
        soft_skills=SoftSkills(leadership=5, autonomy=5, teamwork=5, communication=5),
        tech_stack=TechStack(main=["Python"], secondary=[], veille=[]),
        mobility="Paris",
        weak_signals="None",
        summary="A test CV"
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
    assert data["analysis"]["career_dynamics"]["seniority"] == "Senior"
    assert data["dossier_markdown"] == "# Augmented Dossier"
    
    mock_download.assert_called_once()
    mock_parse.assert_called_once()
    mock_analyzer.analyze_cv.assert_called_once_with("This is the extracted text.")

@patch("app.main.analyzer", None)
def test_analyze_cv_no_analyzer():
    response = client.post("/api/cv/analyze/test-uuid")
    assert response.status_code == 503
    assert "Service d'analyse IA non configuré" in response.json()["detail"]

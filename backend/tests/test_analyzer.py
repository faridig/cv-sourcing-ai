import pytest
from unittest.mock import MagicMock, patch
from app.analyzer import CVAnalyzer
from app.models import AnalyseCV

@pytest.fixture
def mock_openai_response():
    # Mock data following the new AnalyseCV model
    mock_json = {
        "dynamique_carriere": {
            "seniorite": "Sénior", 
            "progression": "Croissance constante",
            "exposition_strategique": "Forte"
        },
        "stack_metier": {
            "principale": ["Python", "FastAPI"], 
            "secondaire": ["Docker"], 
            "veille_et_normes": ["Rust"]
        },
        "fit_culturel": "Agile, Startup",
        "rayonnement": "Actif sur GitHub",
        "competences_douces": {
            "leadership": "A dirigé une équipe de 5 personnes", 
            "autonomie": "Gestion complète du projet X", 
            "travail_equipe": "Évolue en environnement Scrum", 
            "communication": "Rédaction de rapports techniques"
        },
        "langues": ["Français", "Anglais"],
        "localisation": "Paris, 75001",
        "mobilite": "Télétravail total",
        "signaux_faibles": "Parcours cohérent",
        "resume": "Développeur expérimenté.",
        "audit_rigueur": {
            "score_orthographe": "Excellent",
            "coherence_competences": "Élevée",
            "coquilles_detectees": []
        }
    }
    return AnalyseCV.model_validate(mock_json)

@patch("app.analyzer.OpenAI")
def test_analyze_cv_success(mock_openai_class, mock_openai_response):
    # Setup mock
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    mock_completion = MagicMock()
    mock_message = MagicMock()
    mock_message.parsed = mock_openai_response
    mock_message.refusal = None
    mock_completion.choices = [MagicMock(message=mock_message)]
    
    # We mock 'parse' method
    mock_client.chat.completions.parse.return_value = mock_completion
    
    # Execute
    analyzer = CVAnalyzer(api_key="fake-key")
    analysis, markdown = analyzer.analyze_cv("This is a dummy CV text.")
    
    # Assert
    assert isinstance(analysis, AnalyseCV)
    assert analysis.dynamique_carriere.seniorite == "Sénior"
    assert "équipe de 5 personnes" in analysis.competences_douces.leadership
    assert analysis.localisation == "Paris, 75001"
    assert "Dossier Augmenté" in markdown
    assert "Python" in analysis.stack_metier.principale

@patch("app.analyzer.OpenAI")
def test_analyze_cv_refusal(mock_openai_class):
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    mock_completion = MagicMock()
    mock_message = MagicMock()
    mock_message.parsed = None
    mock_message.refusal = "Content too short"
    mock_completion.choices = [MagicMock(message=mock_message)]
    
    mock_client.chat.completions.parse.return_value = mock_completion
    
    analyzer = CVAnalyzer(api_key="fake-key")
    with pytest.raises(RuntimeError, match="IA a refusé d'analyser ce CV"):
        analyzer.analyze_cv("Short text")

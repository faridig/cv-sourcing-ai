import pytest
from unittest.mock import MagicMock, patch
from app.analyzer import CVAnalyzer
from app.models import AnalyseCV

@pytest.fixture
def mock_openai_response():
    mock_json = {
        "dynamique_carriere": {"seniorite": "Sénior", "progression": "Croissance constante dans des rôles backend"},
        "fit_culturel": "Agile, Startup",
        "rayonnement": "Actif sur GitHub, 50 étoiles sur un projet",
        "langues": ["Français (Maternel)", "Anglais (Professionnel)"],
        "competences_douces": {"leadership": 8, "autonomie": 9, "travail_equipe": 7, "communication": 8},
        "stack_technique": {"principale": ["Python", "FastAPI"], "secondaire": ["Docker", "PostgreSQL"], "veille": ["Rust"]},
        "mobilite": "Ouvert au télétravail, basé à Paris",
        "signaux_faibles": "Parcours cohérent, pas de lacunes majeures",
        "localisation": "Paris, 75001",
        "resume": "Développeur Python expérimenté avec de solides compétences en backend."
    }
    
    markdown_content = "# Dossier Augmenté de Test\n\n- **Séniorité**: Sénior\n- **Localisation**: Paris, 75001"
    
    mock_content = f"""```json
    {import_json_as_string(mock_json)}
    ```
    ---MARKDOWN---
    {markdown_content}"""
    
    return mock_content

def import_json_as_string(d):
    import json
    return json.dumps(d)

@patch("app.analyzer.OpenAI")
def test_analyze_cv_success(mock_openai_class, mock_openai_response):
    # Setup mock
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content=mock_openai_response))]
    mock_client.chat.completions.create.return_value = mock_completion
    
    # Execute
    analyzer = CVAnalyzer(api_key="fake-key")
    analysis, markdown = analyzer.analyze_cv("This is a dummy CV text.")
    
    # Assert
    assert isinstance(analysis, AnalyseCV)
    assert analysis.dynamique_carriere.seniorite == "Sénior"
    assert analysis.competences_douces.leadership == 8
    assert analysis.localisation == "Paris, 75001"
    assert "Dossier Augmenté" in markdown
    assert "Python" in analysis.stack_technique.principale

@patch("app.analyzer.OpenAI")
def test_analyze_cv_missing_info(mock_openai_class):
    # Test how it handles missing info
    mock_json = {
        "dynamique_carriere": {"seniorite": "Non déterminé", "progression": "Données insuffisantes"},
        "fit_culturel": "Non déterminé",
        "rayonnement": "Non déterminé",
        "langues": [],
        "competences_douces": {"leadership": 0, "autonomie": 0, "travail_equipe": 0, "communication": 0},
        "stack_technique": {"principale": [], "secondaire": [], "veille": []},
        "mobilite": "Non déterminé",
        "signaux_faibles": "Aucun signal détecté",
        "localisation": "Non déterminé",
        "resume": "CV trop court pour analyse."
    }
    mock_content = f"{import_json_as_string(mock_json)} ---MARKDOWN--- # Dossier Vide"
    
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content=mock_content))]
    mock_client.chat.completions.create.return_value = mock_completion
    
    analyzer = CVAnalyzer(api_key="fake-key")
    analysis, markdown = analyzer.analyze_cv("Short text")
    
    assert analysis.dynamique_carriere.seniorite == "Non déterminé"
    assert "Dossier Vide" in markdown

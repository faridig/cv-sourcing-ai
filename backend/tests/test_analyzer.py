import pytest
from unittest.mock import MagicMock, patch
from app.analyzer import CVAnalyzer
from app.models import CVAnalysis

@pytest.fixture
def mock_openai_response():
    mock_json = {
        "career_dynamics": {"seniority": "Sénior", "progression": "Croissance constante dans des rôles backend"},
        "culture_fit": "Agile, Startup",
        "outreach": "Actif sur GitHub, 50 étoiles sur un projet",
        "languages": ["Français (Maternel)", "Anglais (Professionnel)"],
        "soft_skills": {"leadership": 8, "autonomy": 9, "teamwork": 7, "communication": 8},
        "tech_stack": {"main": ["Python", "FastAPI"], "secondary": ["Docker", "PostgreSQL"], "veille": ["Rust"]},
        "mobility": "Ouvert au télétravail, basé à Paris",
        "weak_signals": "Parcours cohérent, pas de lacunes majeures",
        "location": "Paris, 75001",
        "summary": "Développeur Python expérimenté avec de solides compétences en backend."
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
    assert isinstance(analysis, CVAnalysis)
    assert analysis.career_dynamics.seniority == "Sénior"
    assert analysis.soft_skills.leadership == 8
    assert analysis.location == "Paris, 75001"
    assert "Dossier Augmenté" in markdown
    assert "Python" in analysis.tech_stack.main

@patch("app.analyzer.OpenAI")
def test_analyze_cv_missing_info(mock_openai_class):
    # Test how it handles missing info (should be handled by LLM prompt, but let's check validation)
    mock_json = {
        "career_dynamics": {"seniority": "Non déterminé", "progression": "Données insuffisantes"},
        "culture_fit": "Non déterminé",
        "outreach": "Non déterminé",
        "languages": [],
        "soft_skills": {"leadership": 0, "autonomy": 0, "teamwork": 0, "communication": 0},
        "tech_stack": {"main": [], "secondary": [], "veille": []},
        "mobility": "Non déterminé",
        "weak_signals": "Aucun signal détecté",
        "location": "Non déterminé",
        "summary": "CV trop court pour analyse."
    }
    mock_content = f"{import_json_as_string(mock_json)} ---MARKDOWN--- # Dossier Vide"
    
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content=mock_content))]
    mock_client.chat.completions.create.return_value = mock_completion
    
    analyzer = CVAnalyzer(api_key="fake-key")
    analysis, markdown = analyzer.analyze_cv("Short text")
    
    assert analysis.career_dynamics.seniority == "Non déterminé"
    assert "Dossier Vide" in markdown

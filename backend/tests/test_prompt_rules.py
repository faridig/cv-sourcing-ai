import pytest
from app.models import AnalyseCV, AuditRigueur

def test_model_descriptions_updated():
    schema = AnalyseCV.model_json_schema()
    
    # Check AuditRigueur date rule
    audit_rigueur_schema = schema['$defs']['AuditRigueur']
    coquilles_desc = audit_rigueur_schema['properties']['coquilles_detectees']['description']
    assert "RÈGLE STRICTE SUR LES DATES" in coquilles_desc
    assert "Calcule mathématiquement" in coquilles_desc
    
    # Check AnalyseCV resume rule
    resume_desc = schema['properties']['resume']['description']
    assert "RÈGLE ABSOLUE : NE JAMAIS INVENTER DE CHIFFRES OU DE POURCENTAGES" in resume_desc
    assert "qualitative" in resume_desc

def test_resume_field_no_longer_requires_kpi():
    schema = AnalyseCV.model_json_schema()
    resume_desc = schema['properties']['resume']['description']
    # Ensure the old instruction is gone or modified
    assert "cite au moins 2 chiffres/KPIs" not in resume_desc

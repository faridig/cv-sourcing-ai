import os
import json
import logging
from typing import Tuple, Optional
from openai import OpenAI
from .models import CVAnalysis

logger = logging.getLogger(__name__)

class CVAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        env_key = os.getenv("OPENAI_API_KEY")
        self.api_key = api_key or env_key
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

    def analyze_cv(self, cv_text: str) -> Tuple[CVAnalysis, str]:
        """
        Analyse le texte du CV via LLM et retourne les données structurées et un dossier Markdown.
        """
        prompt = f"""
        Tu es un Auditeur RH Expert. Ta tâche est d'analyser le texte du CV suivant et de fournir une analyse structurée ainsi qu'un "Dossier Augmenté" en Markdown.
        
        ### TEXTE DU CV :
        {cv_text}
        
        ### INSTRUCTIONS :
        Analyse le CV selon ces 9 axes :
        1. Dynamique de Carrière (Séniorité/Progression)
        2. Culture Fit (Startup, Grand Compte, Agile, etc.)
        3. Rayonnement (Open Source, Side Projects, Engagement)
        4. Langues (Usage contextuel)
        5. Soft Skills (Scores 0-10 sur Leadership, Autonomie, Travail d'équipe, Communication)
        6. Stack Technologique (Principal, Secondaire, Veille)
        7. Mobilité & Télétravail
        8. Signaux Faibles (Audit de cohérence)
        9. Localisation (Ville de résidence, Code Postal)
        
        ### FORMAT DE SORTIE :
        Tu dois répondre EXCLUSIVEMENT en Français.
        Tu dois retourner un objet JSON correspondant à la structure suivante, suivi du séparateur "---MARKDOWN---", puis le dossier en Markdown.
        
        Structure JSON :
        {{
            "career_dynamics": {{"seniority": "...", "progression": "..."}},
            "culture_fit": "...",
            "outreach": "...",
            "languages": ["...", "..."],
            "soft_skills": {{"leadership": 0-10, "autonomy": 0-10, "teamwork": 0-10, "communication": 0-10}},
            "tech_stack": {{"main": ["..."], "secondary": ["..."], "veille": ["..."]}},
            "mobility": "...",
            "weak_signals": "...",
            "location": "...",
            "summary": "..."
        }}
        
        Important : Si une information est manquante, n'hallucine pas. Utilise "Non déterminé" ou "Données insuffisantes".
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un assistant RH professionnel spécialisé dans l'analyse technique de CV. Tu t'exprimes exclusivement en Français."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            if content is None:
                raise RuntimeError("LLM returned an empty response.")
            
            if "---MARKDOWN---" in content:
                json_part, markdown_part = content.split("---MARKDOWN---", 1)
            else:
                # Fallback if separator is missing
                logger.warning("Separator ---MARKDOWN--- not found in LLM response.")
                json_part = content
                markdown_part = "# Dossier Augmenté\n\n(Auto-generated from analysis)\n\n" + content

            # Clean JSON part (sometimes LLM adds code blocks)
            json_part = json_part.strip()
            if json_part.startswith("```json"):
                json_part = json_part[7:]
            if json_part.endswith("```"):
                json_part = json_part[:-3]
            json_part = json_part.strip()

            analysis_data = CVAnalysis.model_validate_json(json_part)
            return analysis_data, markdown_part.strip()

        except Exception as e:
            logger.error(f"Error during CV analysis: {str(e)}")
            raise RuntimeError(f"CV analysis failed: {str(e)}")

import os
import json
import logging
from typing import Tuple, Optional
from openai import OpenAI
from .models import AnalyseCV

logger = logging.getLogger(__name__)

class CVAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        env_key = os.getenv("OPENAI_API_KEY")
        self.api_key = api_key or env_key
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

    def analyze_cv(self, cv_text: str) -> Tuple[AnalyseCV, str]:
        """
        Analyse le texte du CV via LLM et retourne les données structurées et un dossier Markdown.
        """
        prompt = f"""
        Tu es un Auditeur RH Expert et Chasseur de Têtes Senior. Ta tâche est d'analyser le texte du CV suivant avec une profondeur analytique maximale.
        
        ### TEXTE DU CV :
        {cv_text}
        
        ### MISSIONS D'AUDIT (LES 5 PILIERS) :
        1. **Chronologie Non-Linéaire** : Analyse les dates pour repérer les chevauchements, les retours d'expérience ou les progressions atypiques.
        2. **Impact KPI** : Identifie les résultats concrets, les chiffres et les verbes d'action. Ne te contente pas de lister les tâches.
        3. **Hiérarchie Hard/Transverse** : Distingue clairement les expertises techniques (Hard) des compétences transversales (Méthodologies, Management).
        4. **Détection fine de Signaux Faibles** : Repère les trous de plus de 6 mois, les changements fréquents d'entreprise ou les incohérences sémantiques.
        5. **Expertise Sectorielle** : Évalue la pertinence du candidat par rapport à ses environnements passés (Startup vs Grand Compte).

        ### FORMAT DE SORTIE :
        Tu dois répondre EXCLUSIVEMENT en Français.
        Tu dois retourner un objet JSON correspondant à la structure définie ci-dessous, suivi du séparateur "---MARKDOWN---", puis un "Dossier Augmenté" détaillé en Markdown.
        
        Structure JSON attendue :
        {{
            "dynamique_carriere": {{
                "seniorite": "Junior|Intermédiaire|Sénior|Lead|Expert", 
                "progression": "Analyse détaillée de la progression et chronologie"
            }},
            "fit_culturel": "Analyse de l'environnement idéal (Startup, Agile, Grand Compte)",
            "rayonnement": "Engagement communautaire, Open Source, Side Projects, Conférences",
            "langues": ["Langue (Niveau/Contexte)", "..."],
            "competences_douces": {{
                "leadership": 0-10, 
                "autonomie": 0-10, 
                "travail_equipe": 0-10, 
                "communication": 0-10
            }},
            "stack_technique": {{
                "principale": ["..."], 
                "secondaire": ["..."], 
                "veille": ["..."]
            }},
            "mobilite": "Zone géographique et télétravail",
            "signaux_faibles": "Audit critique : trous, incohérences, points de vigilance",
            "localisation": "Ville, Code Postal",
            "resume": "Synthèse executive à fort impact"
        }}
        
        Important : Si une information est manquante, n'hallucine pas. Utilise "Non déterminé" ou "Données insuffisantes".
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Tu es un assistant RH professionnel expert en audit de CV. "
                            "Ton analyse doit être critique, structurée et orientée impact (KPI). "
                            "Tu t'exprimes exclusivement en Français."
                        )
                    },
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
                logger.warning("Separator ---MARKDOWN--- not found in LLM response.")
                json_part = content
                markdown_part = "# Dossier Augmenté\n\n(Auto-generated from analysis)\n\n" + content

            # Clean JSON part
            json_part = json_part.strip()
            if json_part.startswith("```json"):
                json_part = json_part[7:]
            if json_part.endswith("```"):
                json_part = json_part[:-3]
            json_part = json_part.strip()

            analysis_data = AnalyseCV.model_validate_json(json_part)
            return analysis_data, markdown_part.strip()

        except Exception as e:
            logger.error(f"Error during CV analysis: {str(e)}")
            raise RuntimeError(f"CV analysis failed: {str(e)}")

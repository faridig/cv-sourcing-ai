import os
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
        Analyse le texte du CV via LLM (Structured Outputs) et retourne les données structurées et un dossier Markdown.
        """
        prompt = f"""
        Tu es un Expert en Audit RH, Psychologue du Travail et Chasseur de Têtes Senior. 
        Ta mission est de déconstruire le texte brut d'un CV pour en extraire une structure logique, objective et exempte de biais.
        
        ### TEXTE DU CV À ANALYSER :
        {cv_text}

        ### PROTOCOLE D'AUDIT (LES 8 AXES) :
        1. **Dynamique de Carrière** : Analyse de la séniorité et de la progression (verticale/horizontale).
        2. **Culture Fit** : Identification de l'environnement idéal (Startup, Grand Groupe, Agile, R&D).
        3. **Rayonnement** : Engagement (Open Source, Conférences, Blogs).
        4. **Langues** : Usage contextuel et niveau déduit.
        5. **Soft Skills (Scores 0-10)** : Évaluation du Leadership, Autonomie, Travail d'équipe et Communication avec scores et preuves.
        6. **Stack Technologique Hiérarchisée** : Distingue Main (cœur), Secondary (outils) et Veille/Normes.
        7. **Mobilité & Télétravail** : Analyse des préférences ou contraintes géographiques citées.
        8. **Signaux Faibles & Audit** : Audit de cohérence, détection de trous, chevauchements ou incohérences.
        """

        try:
            # Utilisation de la méthode 'parse' (OpenAI >= 1.40.0) pour garantir la structure Pydantic
            response = self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Tu es un assistant RH professionnel expert en audit de CV. "
                            "Ton analyse doit être impitoyable, factuelle et orientée impact (KPI). "
                            "Lis attentivement les descriptions de chaque champ dans le schéma JSON pour connaître les contraintes strictes. "
                            "RÈGLE ABSOLUE : NE JAMAIS INVENTER DE CHIFFRES OU DE POURCENTAGES. "
                            "RÈGLE SUR L'ORTHOGRAPHE : IGNORE les noms propres, les technologies, les langages informatiques (ex: Django, PHP, Angular) et pardonne les erreurs de fusion de mots dues à l'extraction PDF (ex: 'Deearning' pour Deep Learning). Ne signale que les vraies fautes de grammaire ou de frappe humaines. "
                            "RÈGLE STRICTE SUR LES DATES (ATTENTION AU PIÈGE CHRONOLOGIQUE) : Les CV sont listés du plus récent au plus ancien. Une expérience qui se termine en '12/2015' et la suivante (plus bas) qui commence en '01/2016' est une suite logique parfaite, il n'y a AUCUN chevauchement. Ne signale une erreur QUE si deux périodes se superposent réellement sur plusieurs mois (ex: un poste de 2016 à 2018 en même temps qu'un autre de 2017 à 2019). "
                            "Si une information n'est pas explicitement présente dans le texte du CV, remplis le champ par 'Non spécifié' ou 'Aucune preuve explicite' selon le contexte. "
                            "Tu t'exprimes exclusivement en Français."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format=AnalyseCV,
                temperature=0.1
            )
            
            analysis_data = response.choices[0].message.parsed
            
            if not analysis_data:
                # Gestion du cas où le modèle refuse de répondre (refusal)
                refusal = response.choices[0].message.refusal
                logger.error(f"LLM refusal: {refusal}")
                raise RuntimeError(f"L'IA a refusé d'analyser ce CV : {refusal}")

            # Génération du Markdown côté serveur
            markdown_part = self._generate_markdown(analysis_data)

            return analysis_data, markdown_part

        except Exception as e:
            logger.error(f"Error during CV analysis: {str(e)}")
            raise RuntimeError(f"CV analysis failed: {str(e)}")

    def _generate_markdown(self, data: AnalyseCV) -> str:
        """Génère un rapport Markdown structuré à partir des données validées."""
        md = f"""# 📑 Dossier Augmenté - Audit RH Expert
        
## 🎯 Synthèse Executive
{data.resume}

## 📈 Dynamique de Carrière
- **Séniorité** : {data.dynamique_carriere.seniorite}
- **Progression** : {data.dynamique_carriere.progression}
- **Exposition Stratégique** : {data.dynamique_carriere.exposition_strategique}

## 🛠️ Expertise & Stack Métier
- **Cœur de métier (Hard Skills)** : {', '.join(data.stack_metier.principale) if data.stack_metier.principale else 'Non spécifié'}
- **Compétences Transverses** : {', '.join(data.stack_metier.secondaire) if data.stack_metier.secondaire else 'Non spécifié'}
- **Veille & Normes** : {', '.join(data.stack_metier.veille_et_normes) if data.stack_metier.veille_et_normes else 'Non spécifié'}

## 🧠 Compétences Douces (Scores & Preuves)
- 👑 **Leadership** : {data.competences_douces.leadership.score}/10 - {data.competences_douces.leadership.preuve}
- 🚀 **Autonomie** : {data.competences_douces.autonomie.score}/10 - {data.competences_douces.autonomie.preuve}
- 🤝 **Travail d'équipe** : {data.competences_douces.travail_equipe.score}/10 - {data.competences_douces.travail_equipe.preuve}
- 🗣️ **Communication** : {data.competences_douces.communication.score}/10 - {data.competences_douces.communication.preuve}

## 🌍 Fit Culturel & Rayonnement
- **Environnement idéal** : {data.fit_culturel}
- **Rayonnement / Engagement** : {data.rayonnement}

## 📍 Informations Pratiques
- **Localisation** : {data.localisation}
- **Mobilité & Télétravail** : {data.mobilite}
- **Langues** : {', '.join(data.langues) if data.langues else 'Non déterminé'}

## 🔍 Audit de Rigueur & Signaux Faibles
- **Audit de cohérence** : {data.signaux_faibles}
- **Qualité rédactionnelle** : {data.audit_rigueur.score_orthographe}
- **Cohérence Rôles/Compétences** : {data.audit_rigueur.coherence_competences}
"""
        if data.audit_rigueur.coquilles_detectees:
            md += "\n**Points de vigilance :**\n"
            for coquille in data.audit_rigueur.coquilles_detectees:
                md += f"- {coquille}\n"
        
        return md.strip()

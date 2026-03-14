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

        ### PROTOCOLE D'AUDIT (LES 5 PILIERS) :
        1. **Chronologie Non-Linéaire** : Calcule la durée réelle des expériences. Repère les chevauchements, les retours d'expérience ou les progressions atypiques (verticales/horizontales).
        2. **Impact KPI (Valeur Ajoutée)** : Isole les PREUVES concrètes de succès (chiffres, verbes d'action, résultats). Ne te contente pas de lister les tâches.
        3. **Hiérarchie Hard/Transverse** : Distingue clairement les expertises techniques (Hard) des compétences transversales (Méthodologies, Management, Transversalité).
        4. **Détection fine de Signaux Faibles** : Traque les trous de plus de 6 mois, les changements fréquents d'entreprise ou les incohérences sémantiques entre le titre et le contenu.
        5. **Expertise & Rigueur** : Évalue la qualité rédactionnelle et la cohérence globale du parcours.
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
                            "RÈGLE ABSOLUE : Tu es pénalisé si tu hallucines ou inventes des informations. Si une information n'est pas explicitement présente dans le texte du CV, remplis le champ par 'Non spécifié'. "
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

## 🧠 Compétences Douces (Scores /10)
- 🗣️ **Communication** : {data.competences_douces.communication}/10
- 🤝 **Travail d'équipe** : {data.competences_douces.travail_equipe}/10
- 🚀 **Autonomie** : {data.competences_douces.autonomie}/10
- 👑 **Leadership** : {data.competences_douces.leadership}/10

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

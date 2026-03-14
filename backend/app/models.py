from pydantic import BaseModel, Field
from typing import List, Optional

class StackMetier(BaseModel):
    principale: List[str] = Field(
        description="INTERDICTION D'INVENTER. Liste uniquement les expertises techniques majeures explicitement citées dans le CV."
    )
    secondaire: List[str] = Field(
        description="Outils et compétences secondaires. Si non mentionné, laisser vide. NE PAS extrapoler."
    )
    veille_et_normes: List[str] = Field(
        description="Normes (ISO, etc.), certifications ou technos en veille. EXCLUSIVEMENT ce qui est écrit."
    )

class CompetencesDouces(BaseModel):
    leadership: int = Field(description="Score 0-10. Sois sévère. 0 si aucune preuve de management ou d'initiative.", ge=0, le=10)
    autonomie: int = Field(description="Score 0-10. Basé sur les projets gérés seul. Pas de preuve = score faible.", ge=0, le=10)
    travail_equipe: int = Field(description="Score 0-10. Basé sur les environnements collaboratifs cités.", ge=0, le=10)
    communication: int = Field(description="Score 0-10. Basé sur les présentations, rapports ou rôles d'interface.", ge=0, le=10)

class DynamiqueCarriere(BaseModel):
    seniorite: str = Field(description="Junior, Intermédiaire, Sénior, Lead, Expert. Basé sur les ANNÉES RÉELLES et responsabilités.")
    progression: str = Field(description="Analyse de la trajectoire. SI TROU DE 6 MOIS : le mentionner ici comme 'ALERTE'.")
    exposition_strategique: str = Field(description="Fait-il de l'exécution pure ou de la stratégie ? Justifie par un fait du CV.")

class AuditRigueur(BaseModel):
    score_orthographe: str = Field(description="Évaluation impitoyable de la langue et de la mise en forme.")
    coherence_competences: str = Field(description="Vérifie si les technos citées correspondent aux dates/rôles. Démasque les mensonges probables.")
    coquilles_detectees: List[str] = Field(
        description=(
            "Liste exhaustive des fautes d'orthographe ou incohérences de dates. "
            "RÈGLE STRICTE SUR LES DATES : Calcule mathématiquement les mois et années avant de signaler un chevauchement. "
            "Ne signale pas de chevauchement si une expérience suit l'autre logiquement (ex: fin en Octobre, début en Octobre). "
            "Vide si parfait."
        )
    )

class AnalyseCV(BaseModel):
    dynamique_carriere: DynamiqueCarriere
    stack_metier: StackMetier
    fit_culturel: str = Field(description="Startup, Grand Compte ou PME ? Justifie par l'historique. NE PAS deviner.")
    rayonnement: str = Field(description="Preuves publiques : GitHub, Blogs, Conférences. Si rien n'est écrit, écrire 'Néant'.")
    competences_douces: CompetencesDouces
    langues: List[str] = Field(description="Langues et niveaux. NE PAS ajouter de langues non citées.")
    localisation: str = Field(description="Ville et CP. Si absent : 'Inconnu'.")
    mobilite: str = Field(description="Mentionne UNIQUEMENT si spécifié (ex: 'Déplacement 50%'). Sinon 'Non précisé'.")
    signaux_faibles: str = Field(description="ZONE CRITIQUE : Analyse les anomalies, les durées trop courtes (<1 an) et les incohérences.")
    resume: str = Field(
        description=(
            "Synthèse IMPACTANTE. Utilise des verbes d'action. "
            "RÈGLE ABSOLUE : NE JAMAIS INVENTER DE CHIFFRES OU DE POURCENTAGES. "
            "Si le CV ne contient pas de métriques exactes, décris les réalisations de manière purement qualitative."
        )
    )
    audit_rigueur: AuditRigueur

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
    leadership: str = Field(description="Preuve concrète de leadership (ex: management, initiative). Si aucune preuve, écrire 'Aucune preuve explicite'.")
    autonomie: str = Field(description="Preuve concrète d'autonomie (ex: gestion de projet en solo). Si aucune preuve, écrire 'Aucune preuve explicite'.")
    travail_equipe: str = Field(description="Preuve concrète de travail d'équipe (ex: environnement collaboratif, agile). Si aucune preuve, écrire 'Aucune preuve explicite'.")
    communication: str = Field(description="Preuve concrète de communication (ex: présentations, rapports). Si aucune preuve, écrire 'Aucune preuve explicite'.")

class DynamiqueCarriere(BaseModel):
    seniorite: str = Field(description="Junior, Intermédiaire, Sénior, Lead, Expert. Basé sur les ANNÉES RÉELLES et responsabilités.")
    progression: str = Field(description="Analyse l'évolution des titres de postes pour déterminer la progression (ex: Analyste -> Data Scientist = Progression verticale ascendante). SI TROU DE 6 MOIS : le mentionner ici comme 'ALERTE'.")
    exposition_strategique: str = Field(description="Fait-il de l'exécution pure ou de la stratégie ? Justifie par un fait du CV.")


class AuditRigueur(BaseModel):
    score_orthographe: str = Field(description="Évaluation de la qualité rédactionnelle. IGNORE les noms propres, les technologies et les langages informatiques. Pardonne les erreurs de fusion de mots dues à l'extraction PDF.")
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
    fit_culturel: str = Field(description="Analyse du type d'environnement idéal (R&D, Opérationnel, International, Agile, etc.). Ne tire pas de conclusion hâtive sur la taille de l'entreprise (PME/Grand Groupe) si ce n'est pas explicitement spécifié. Justifie par les types de projets.")
    rayonnement: str = Field(description="Preuves publiques : GitHub, Blogs, Conférences. Si rien n'est écrit, écrire 'Néant'.")
    competences_douces: CompetencesDouces
    langues: List[str] = Field(description="Langues et niveaux. Si la rubrique n'existe pas, déduis la langue principale utilisée dans la rédaction du CV.")
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

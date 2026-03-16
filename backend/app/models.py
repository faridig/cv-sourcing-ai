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

class CompetenceScore(BaseModel):
    score: int = Field(ge=0, le=10, description="Score de 0 à 10 basé uniquement sur les preuves du CV.")
    preuve: str = Field(description="Preuve concrète extraite du texte. Si aucune, 'Aucune preuve explicite'.")

class CompetencesDouces(BaseModel):
    leadership: CompetenceScore
    autonomie: CompetenceScore
    travail_equipe: CompetenceScore
    communication: CompetenceScore

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
            "RÈGLE STRICTE SUR LES DATES (PIÈGE CHRONOLOGIQUE) : Les CV sont listés du plus récent au plus ancien. "
            "Une expérience qui se termine en '12/2015' et la suivante qui commence en '01/2016' est une suite logique parfaite, il n'y a AUCUN chevauchement. "
            "Ne signale une erreur QUE si deux périodes se superposent réellement sur plusieurs mois. "
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

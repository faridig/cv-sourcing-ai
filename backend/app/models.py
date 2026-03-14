from pydantic import BaseModel, Field
from typing import List, Optional

class StackMetier(BaseModel):
    principale: List[str] = Field(description="Expertises et outils principaux (Hard Skills)")
    secondaire: List[str] = Field(description="Outils et compétences secondaires ou transverses")
    veille_et_normes: List[str] = Field(description="Technologies en veille, normes du secteur ou certifications")

class CompetencesDouces(BaseModel):
    leadership: int = Field(description="Score de 0 à 10", ge=0, le=10)
    autonomie: int = Field(description="Score de 0 à 10", ge=0, le=10)
    travail_equipe: int = Field(description="Score de 0 à 10", ge=0, le=10)
    communication: int = Field(description="Score de 0 à 10", ge=0, le=10)

class DynamiqueCarriere(BaseModel):
    seniorite: str = Field(description="Junior, Intermédiaire, Sénior, Lead, Expert")
    progression: str = Field(description="Analyse de la progression (Verticale/Horizontale)")
    exposition_strategique: str = Field(description="Niveau d'implication dans la stratégie vs exécution")

class AuditRigueur(BaseModel):
    score_orthographe: str = Field(description="Évaluation de la qualité rédactionnelle")
    coherence_competences: str = Field(description="Vérification de l'adéquation entre rôles et outils cités")
    coquilles_detectees: List[str] = Field(description="Liste des points de vigilance ou erreurs relevées")

class AnalyseCV(BaseModel):
    dynamique_carriere: DynamiqueCarriere
    stack_metier: StackMetier
    fit_culturel: str = Field(description="Environnement idéal (Startup, Grand Compte, Secteur Public, etc.)")
    rayonnement: str = Field(description="Engagement (Open Source, Side Projects, Conférences, etc.)")
    competences_douces: CompetencesDouces
    langues: List[str] = Field(description="Maîtrise linguistique en contexte professionnel")
    localisation: str = Field(description="Ville et Code Postal")
    mobilite: str = Field(description="Rayon géographique et préférences de télétravail")
    signaux_faibles: str = Field(description="Points de vigilance (trous > 6 mois, changements fréquents, etc.)")
    resume: str = Field(description="Synthèse executive avec mise en avant des KPIs et verbes d'action")
    audit_rigueur: AuditRigueur

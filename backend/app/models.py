from pydantic import BaseModel, Field
from typing import List, Optional

class StackTechnique(BaseModel):
    principale: List[str] = Field(description="Technologies et frameworks principaux")
    secondaire: List[str] = Field(description="Technologies et outils secondaires")
    veille: List[str] = Field(description="Technologies en veille ou intérêt émergent")

class CompetencesDouces(BaseModel):
    leadership: int = Field(description="Score de 0 à 10", ge=0, le=10)
    autonomie: int = Field(description="Score de 0 à 10", ge=0, le=10)
    travail_equipe: int = Field(description="Score de 0 à 10", ge=0, le=10)
    communication: int = Field(description="Score de 0 à 10", ge=0, le=10)

class DynamiqueCarriere(BaseModel):
    seniorite: str = Field(description="Junior, Intermédiaire, Sénior, Lead, Expert")
    progression: str = Field(description="Description de la progression de carrière et chronologie")

class AnalyseCV(BaseModel):
    dynamique_carriere: DynamiqueCarriere
    fit_culturel: str = Field(description="Startup, Grand Compte, Agile, etc.")
    rayonnement: str = Field(description="Open Source, Side Projects, Engagement")
    langues: List[str] = Field(description="Usage contextuel des langues")
    competences_douces: CompetencesDouces
    stack_technique: StackTechnique
    mobilite: str = Field(description="Mobilité et préférences de télétravail")
    signaux_faibles: str = Field(description="Audit de cohérence, trous dans le CV, et signaux faibles")
    localisation: str = Field(description="Ville de résidence et code postal")
    resume: str = Field(description="Résumé exécutif court")

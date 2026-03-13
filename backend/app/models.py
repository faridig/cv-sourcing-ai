from pydantic import BaseModel, Field
from typing import List, Optional

class TechStack(BaseModel):
    main: List[str] = Field(description="Primary technologies and frameworks")
    secondary: List[str] = Field(description="Secondary technologies and tools")
    veille: List[str] = Field(description="Technologies for monitoring or emerging interest")

class SoftSkills(BaseModel):
    leadership: int = Field(description="Score from 0 to 10", ge=0, le=10)
    autonomy: int = Field(description="Score from 0 to 10", ge=0, le=10)
    teamwork: int = Field(description="Score from 0 to 10", ge=0, le=10)
    communication: int = Field(description="Score from 0 to 10", ge=0, le=10)

class CareerDynamics(BaseModel):
    seniority: str = Field(description="Junior, Mid, Senior, Lead, Expert")
    progression: str = Field(description="Description of career growth")

class CVAnalysis(BaseModel):
    career_dynamics: CareerDynamics
    culture_fit: str = Field(description="Startup, Grand Compte, Agile, etc.")
    outreach: str = Field(description="Open Source, Side Projects, Engagement")
    languages: List[str] = Field(description="Contextual usage of languages")
    soft_skills: SoftSkills
    tech_stack: TechStack
    mobility: str = Field(description="Mobility and Teleworking preferences")
    weak_signals: str = Field(description="Consistency audit and weak signals")
    summary: str = Field(description="Short executive summary")

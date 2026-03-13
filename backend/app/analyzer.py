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
        Analyzes the CV text using LLM and returns both structured data and a Markdown dossier.
        """
        prompt = f"""
        You are an expert HR Auditor. Your task is to analyze the following CV text and provide a structured analysis and an "Augmented Dossier" in Markdown.
        
        ### CV TEXT:
        {cv_text}
        
        ### INSTRUCTIONS:
        Analyze the CV across these 8 axes:
        1. Career Dynamics (Seniority/Progression)
        2. Culture Fit (Startup/Grand Compte/Agile)
        3. Outreach (Open Source/Side Projects/Engagement)
        4. Languages (Contextual usage)
        5. Soft Skills (Scores 0-10 on Leadership, Autonomy, Teamwork, Communication)
        6. Tech Stack (Main, Secondary, Monitoring/Veille)
        7. Mobility & Teleworking
        8. Weak Signals (Consistency audit)
        
        ### OUTPUT FORMAT:
        You must return a JSON object that matches the following structure, followed by a separator "---MARKDOWN---" and then the Markdown dossier.
        
        JSON Structure:
        {{
            "career_dynamics": {{"seniority": "...", "progression": "..."}},
            "culture_fit": "...",
            "outreach": "...",
            "languages": ["...", "..."],
            "soft_skills": {{"leadership": 0-10, "autonomy": 0-10, "teamwork": 0-10, "communication": 0-10}},
            "tech_stack": {{"main": ["..."], "secondary": ["..."], "veille": ["..."]}},
            "mobility": "...",
            "weak_signals": "...",
            "summary": "..."
        }}
        
        Important: If information is missing, do not hallucinate. Use "Non déterminé" or "Données insuffisantes".
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional HR assistant specializing in technical CV analysis."},
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

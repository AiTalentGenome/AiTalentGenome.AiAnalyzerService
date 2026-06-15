from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class MotivationBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Оценка мотивации и профессиональной самооценки'.
    Входит в родительский блок 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist and Executive Profiler.\n"
            "Your task is to analyze the candidate's career motivation, internal drivers, and professional self-esteem based ONLY on the verified data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract real facts strictly from the <candidate_resume> and <candidate_cover_letter> tags. Do not assume or extrapolate professional ambition.\n"
            "2. If the text does not contain clear indicators for a specific key, return an empty array [] for that key.\n"
            "3. NEVER reuse, echo, or rewrite phrases, technical skills, or concepts listed in these system instructions in your JSON output.\n"
            "4. THIRD PERSON RULE: Strictly write all descriptions in the THIRD PERSON (e.g., 'Кандидат ориентирован', 'Сотрудник стремится'). Writing from the first person ('I', 'Me', 'Я', 'Мой опыт') is STRICTLY FORBIDDEN.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All elements inside arrays must be written strictly in RUSSIAN.\n"
            "4. Avoid nested arrays; output a clean, flat list of strings for each array key.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [],\n'  # Схема полностью очищена — Qwen заполнит массивы сам
            '  "resume_manifestation": [],\n'
            '  "conclusion_points": []\n'
            "}"
        )
    
    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает массивы манифестации мотивации и самооценки кандидатов.
        """
        return {
            "interview_manifestation": list(raw_json.get("interview_manifestation", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion_points": list(raw_json.get("conclusion_points", []))
        }
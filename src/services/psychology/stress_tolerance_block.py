from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class StressToleranceBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Уровень стрессоустойчивости и способность к принятию решений'.
    Входит в родительский блок 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist, Risk Manager, and Crisis Assessor.\n"
            "Your task is to analyze the candidate's stress tolerance, emotional control, and decision-making patterns under pressure based ONLY on the verified data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract real behavioral facts strictly from the <candidate_resume> and <candidate_cover_letter> tags. Do not invent crisis experiences.\n"
            "2. If the context lacks explicit stress indicators or crisis stories, return an empty array [] for that specific key.\n"
            "3. NEVER reuse, copy, or adapt phrases or examples from these system instructions in your JSON output.\n"
            "4. THIRD PERSON RULE: Strictly write all descriptions in the THIRD PERSON (e.g., 'Кандидат проявляет хладнокровие', 'Сотрудник склонен к'). Writing from the first person ('Я', 'Мой') is STRICTLY FORBIDDEN.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All values in arrays must be written strictly in RUSSIAN.\n"
            "4. Avoid nested arrays; output a clean, flat list of strings for each array key.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [],\n'  # Схема очищена — Qwen заполнит её на основе названий ключей
            '  "resume_manifestation": [],\n'
            '  "conclusion_points": []\n'
            "}"
        )
    
    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает массивы поведенческих индикаторов стрессоустойчивости.
        """
        return {
            "interview_manifestation": list(raw_json.get("interview_manifestation", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion_points": list(raw_json.get("conclusion_points", []))
        }
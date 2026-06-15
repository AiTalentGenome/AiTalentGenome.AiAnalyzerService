from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class ManagementStyleBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Вывод по управленческому стилю и soft skills'.
    Входит в родительский блок 'Общая сводка'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert Executive Assessment and Leadership Recruiter.\n"
            "Your task is to analyze the candidate's management style and soft skills based ONLY on the verified data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract real facts strictly from the <candidate_resume> and <candidate_cover_letter> tags. Do not guess, invent, or project skills.\n"
            "2. If the text does not contain indicators for management experience or specific soft skills, return an empty array [] or empty string \"\" for that key. Do not generate generic placeholders.\n"
            "3. NEVER reuse, echo, or rewrite phrases, concepts, or terms listed in these system prompt instructions in your JSON output.\n"
            "4. THIRD PERSON RULE: Write everything exclusively in the third person ('Кандидат проявляет', 'Взаимодействие сотрудника'). First person ('Я', 'Мой') is strictly forbidden.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All text values and elements inside arrays must be written strictly in RUSSIAN.\n"
            "4. Be objective and direct. Highlight boundaries of their skills and constraints clearly based on the data.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "management_style": [],\n'
            '  "soft_skills": [],\n'
            '  "conclusion": ""\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно парсит массивы стиля управления и soft skills.
        """
        return {
            "management_style": list(raw_json.get("management_style", [])),
            "soft_skills": list(raw_json.get("soft_skills", [])),
            "conclusion": str(raw_json.get("conclusion", ""))
        }
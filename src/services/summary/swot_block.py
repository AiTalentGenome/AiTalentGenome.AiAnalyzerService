from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class SwotBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'SWOT-анализ кандидата'.
    Входит в родительский блок 'Общая сводка'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Strategist, Corporate Risk Manager, and Talent Assessor.\n"
            "Your task is to conduct a professional, rigorous SWOT analysis of the candidate relative to the target vacancy based ONLY on the verified data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract analytical facts strictly from the <candidate_resume> and <candidate_cover_letter> tags. Compare them strictly with <target_vacancy>.\n"
            "2. Do not invent strengths, assume business opportunities, or guess hidden threats. If factual data is missing for a specific quadrant, return an empty array [] for that key.\n"
            "3. NEVER reuse, echo, or rephrase terms, placeholder words, or descriptive sentences listed in these system instructions in your JSON output.\n"
            "4. THIRD PERSON RULE: Write the entire analysis exclusively in the third person ('Кандидат обладает', 'У сотрудника выявлен пробел'). First person ('Я', 'Мой') is strictly forbidden.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All elements inside arrays must be written strictly in RUSSIAN.\n"
            "4. Avoid nested arrays; output a clean, flat list of strings for each array key.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "strengths": [],\n'  # Схема полностью пустая — Qwen заполнит её на основе ключей
            '  "weaknesses": [],\n'
            '  "opportunities": [],\n'
            '  "threats": []\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает все 4 списка SWOT-матрицы.
        """
        return {
            "strengths": list(raw_json.get("strengths", [])),
            "weaknesses": list(raw_json.get("weaknesses", [])),
            "opportunities": list(raw_json.get("opportunities", [])),
            "threats": list(raw_json.get("threats", []))
        }
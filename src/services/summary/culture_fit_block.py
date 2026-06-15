from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class CultureFitBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Анализ ценностного совпадения'.
    Входит в родительский блок 'Общая сводка' и оценивает Culture Fit.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Corporate Culture Analyst and Values Matcher.\n"
            "Your task is to analyze how well the candidate aligns with corporate values based ONLY on the verified data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract real values and opinions strictly from <target_vacancy>, <candidate_resume>, and <candidate_cover_letter> tags. Do not assume or invent expectations.\n"
            "2. If the text context does not provide sufficient data to analyze corporate values or candidate opinion, return empty arrays [] for those keys.\n"
            "3. NEVER reuse, echo, or copy example values or instructional terms from this system prompt in your JSON output.\n"
            "4. THIRD PERSON RULE: Write all text fields and strings exclusively in the third person (e.g., 'Кандидат разделяет', 'Взгляды сотрудника'). First person ('Я', 'Мой') is strictly forbidden.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All text values, strings, and elements in arrays must be written strictly in RUSSIAN.\n"
            "4. The 'culture_fit_score' must be a dynamically calculated float between 0.0 and 1.0 based strictly on objective alignment.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "culture_fit_score": 0.0,\n'
            '  "company_values": [],\n'  
            '  "candidate_opinion": [],\n'
            '  "alignments": [],\n'
            '  "cultural_risks": [],\n'
            '  "conclusion": ""\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно парсит и структурирует данные для UI-блока ценностей.
        """
        return {
            "culture_fit_score": float(raw_json.get("culture_fit_score", 0.0)),
            "company_values": list(raw_json.get("company_values", [])),  # Вычистили дефолтный хардкод
            "candidate_opinion": list(raw_json.get("candidate_opinion", [])),
            "alignments": list(raw_json.get("alignments", [])),
            "cultural_risks": list(raw_json.get("cultural_risks", [])),
            "conclusion": str(raw_json.get("conclusion", ""))
        }
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
            "Your task is to analyze the candidate's management style and soft skills based on their experience and interview data.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullets, and descriptions must be strictly in RUSSIAN.\n"
            "3. Be objective and direct. Highlight boundaries of their skills (e.g., if they are structured but not flexible, state it clearly).\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "management_style": [\n'
            '    "Особенности стиля управления (например: Жесткий, но справедливый – требует дисциплины)",\n'
            '    "Ориентация в работе (например: Ориентирован на результат, а не на поиск компромиссов)"\n'
            '  ],\n'
            '  "soft_skills": [\n'
            '    "Коммуникация (например: Коммуникация без лишних эмоций, уверенная – говорит по делу)",\n'
            '    "Гибкость / Обучаемость (например: Четко выражает мысли, но не всегда гибок в общении)"\n'
            '  ],\n'
            '  "conclusion": "Итоговый сжатый вывод (например: Кандидат сильный управленец, требовательный, но не склонен к гибкости)"\n'
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
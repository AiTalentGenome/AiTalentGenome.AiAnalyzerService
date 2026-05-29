from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class FinalVerdictBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Общий вывод'.
    Финиширует родительский блок 'Общая сводка'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Chief Human Resources Officer (CHRO) and Senior Talent Acquisition Executive.\n"
            "Your task is to write a final executive verdict and onboarding recommendations for the hiring manager based on the overall candidate data.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text descriptions, bullets, and fields must be strictly in RUSSIAN.\n"
            "3. Provide realistic, actionable advice for onboarding and potential risks.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "verdict": "Главное текстовое резюме (например: Кандидат – опытный руководитель, отлично понимающий процессы...)",\n'
            '  "pros": [\n'
            '    "Что делает его хорошим кандидатом (например: Опыт управления коллективами и процессами)",\n'
            '    "Чёткое понимание планирования, сроков и ТБ"\n'
            '  ],\n'
            '  "to_consider": [\n'
            '    "Что учитывать / Зоны внимания (например: Жёсткий стиль управления – важно, насколько коллектив готов)",\n'
            '    "Чтение чертежей требует восстановления навыков"\n'
            '  ],\n'
            '  "recommendation": "Итоговая рекомендация по найму и адаптации кандидата в компании."\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно парсит финальный вердикт и рекомендации.
        """
        return {
            "verdict": str(raw_json.get("verdict", "")),
            "pros": list(raw_json.get("pros", [])),
            "to_consider": list(raw_json.get("to_consider", [])),
            "recommendation": str(raw_json.get("recommendation", ""))
        }
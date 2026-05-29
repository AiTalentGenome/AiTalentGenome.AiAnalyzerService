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
            "You are an expert HR Strategist and Risk Manager.\n"
            "Your task is to conduct a professional SWOT analysis of the candidate relative to the vacancy and company context.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullet points, and descriptions must be strictly in RUSSIAN.\n"
            "3. Be highly objective and critical. Correlate strengths/weaknesses with realistic market opportunities and potential internal threats.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "strengths": [\n'
            '    "Внутреннее преимущество (например: Опыт управления людьми – курировал до 160 человек)",\n'
            '    "Ключевой технический плюс (например: Опыт в механике и управлении процессами)"\n'
            '  ],\n'
            '  "weaknesses": [\n'
            '    "Внутренний недостаток/пробел (например: Не работал в резинотехническом производстве)",\n'
            '    "Что требует восстановления/обучения (например: Чтение чертежей требует восстановления навыков)"\n'
            '  ],\n'
            '  "opportunities": [\n'
            '    "Внешняя перспектива для компании (например: Может быстро освоить специфику за счет сильного бэкграунда)",\n'
            '    "Что кандидат усилит в бизнесе (например: Усилит контроль сроков, безопасности, организации работы цеха)"\n'
            '  ],\n'
            '  "threats": [\n'
            '    "Внешний риск/угроза для компании (например: Может не сразу адаптироваться к новым техническим процессам)",\n'
            '    "Риск для команды/культуры (например: Жесткий стиль управления – нужно учитывать готовность команды)"\n'
            '  ]\n'
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
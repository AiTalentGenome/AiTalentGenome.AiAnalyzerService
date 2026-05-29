from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class SummaryBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Краткое резюме интервью (саммари)'.
    Входит в родительский блок 'Общая сводка' и генерирует структурированные инсайты.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Analyst. Your task is to create a short, structured summary of the candidate based on their interview data and resume.\n"
            "You must group key aspects into logical categories (e.g., Карьерный путь, Чтение чертежей, Производственный опыт, etc.) and write a concise conclusion.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, aspect keys, and descriptions must be strictly in RUSSIAN.\n"
            "3. Be specific, concise, and professional. Avoid generic phrases.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "ai_summary_text": "Общий сжатый текст для быстрого ознакомления (1-2 предложения)",\n'
            '  "key_aspects": {\n'
            '    "Карьерный путь": "Краткое описание траектории (например: прошёл от механика до руководителя...)",\n'
            '    "Чтение чертежей": "Статус навыка или проблемы (например: ранее использовал, но из-за перерыва возникли трудности...)",\n'
            '    "Производственный опыт": "Специфика опыта (например: не работал с резинотехническими изделиями, но имеет представление...)"\n'
            '  },\n'
            '  "conclusion": "Итоговый вывод (например: Кандидат силён в управлении людьми, но потребуется адаптация...)"\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Гарантирует безопасное извлечение и маппинг полей саммари.
        """
        return {
            "ai_summary_text": str(raw_json.get("ai_summary_text", "")),
            "key_aspects": dict(raw_json.get("key_aspects", {})),
            "conclusion": str(raw_json.get("conclusion", ""))
        }
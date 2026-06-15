from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class SummaryBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Краткое саммари кандидата'.
    Оптимизирован под Qwen 2.5 14B: убраны плейсхолдеры в схеме, добавлена XML-изоляция.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert Executive Recruiter and Technical Talent Sourcer.\n"
            "Your task is to synthesize a high-level, strictly objective brief summary of the candidate based ONLY on the validated data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract and summarize real facts, metrics, and statements strictly from the <candidate_resume> and <candidate_cover_letter> tags.\n"
            "2. Cross-reference the candidate's data with <target_vacancy>. If there is a total mismatch (e.g., a SysAdmin applying for a Sales role), state it directly and objectively without trying to smooth it over.\n"
            "3. Absolute prohibition on hallucinating technical skills, achievements, or management scales that are not explicitly present in the candidate's text.\n"
            "4. Never inject any terms, technologies, or concepts from these system prompt instructions into your analytical output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory.\n"
            "3. All text values, summary paragraphs, and keys inside 'key_aspects' must be written strictly in RUSSIAN.\n"
            "4. THIRD PERSON RULE: Write everything exclusively in the third person ('Кандидат обладает', 'Опыт сотрудника'). First person ('Я', 'Мой') is strictly forbidden.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "ai_summary_text": "",\n'
            '  "key_aspects": {\n'
            '    "Управленческий масштаб": "",\n'
            '    "Технический бэкграунд": "",\n'
            '    "Поведенческие маркеры и стресс": "",\n'
            '    "Прагматика и стабильность": ""\n'
            '  },\n'
            '  "conclusion": ""\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает текстовые поля саммари и словарь ключевых аспектов.
        """
        key_aspects = raw_json.get("key_aspects", {})
        if not isinstance(key_aspects, dict):
            key_aspects = {}
            
        return {
            "ai_summary_text": str(raw_json.get("ai_summary_text", "")),
            "key_aspects": {
                "Управленческий масштаб": str(key_aspects.get("Управленческий масштаб", "")),
                "Технический бэкграунд": str(key_aspects.get("Технический бэкграунд", "")),
                "Поведенческие маркеры и стресс": str(key_aspects.get("Поведенческие маркеры и стресс", "")),
                "Прагматика и стабильность": str(key_aspects.get("Прагматика и стабильность", ""))
            },
            "conclusion": str(raw_json.get("conclusion", ""))
        }
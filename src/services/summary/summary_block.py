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
            "You are an expert HR Analyst. Your task is to create a short, highly structured summary of the candidate based on the provided interview data and resume.\n"
            "You must extract key professional aspects into logical, candidate-specific categories and write a concise conclusion.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. Do not inventory generic categories. Extract fields for 'key_aspects' dynamically based ONLY on what is relevant to this specific candidate's actual background.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All text values, dictionary keys in 'key_aspects', and descriptions must be strictly in RUSSIAN.\n"
            "4. Be specific, concise, and professional. Avoid generic phrases.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "ai_summary_text": "<общий_сжатый_текст_резюме_для_быстрого_ознакомления_строго_1_2_предложения>",\n'
            '  "key_aspects": {\n'
            '    "<Динамическое_Название_Категории_1>": "<фактический_анализ_первого_важного_аспекта_опыта_кандидата>",\n'
            '    "<Динамическое_Название_Категории_2>": "<фактический_анализ_второго_важного_аспекта_опыта_кандидата>"\n'
            '  },\n'
            '  "conclusion": "<итоговый_емкий_вывод_о_готовности_кандидата_к_работе_и_нюансах_его_онбординга>"\n'
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
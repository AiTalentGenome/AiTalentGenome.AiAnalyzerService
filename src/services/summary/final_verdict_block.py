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
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] or an empty string \"\" for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All values in arrays and strings must be written strictly in RUSSIAN.\n"
            "4. Do not limit the number of items in arrays; generate as many analytical bullet points as objectively supported by the source text.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "verdict": "<главное_итоговое_текстовое_резюме_о_соответствии_кандидата_должности_его_потенциале_и_общем_впечатлении>",\n'
            '  "pros": [\n'
            '    "<ключевое_преимущество_кандидата_выделенное_из_его_реального_опыта_и_навыков>",\n'
            '    "<дополнительные_сильные_стороны_и_факторы_успешности_в_данной_роли>"\n'
            '  ],\n'
            '  "to_consider": [\n'
            '    "<критические_зоны_внимания_риски_или_недостающие_компетенции_подтвержденные_текстом>",\n'
            '    "<поведенческие_или_технические_нюансы_которые_потребуют_контроля_со_стороны_нанимающего_менеджера>"\n'
            '  ],\n'
            '  "recommendation": "<развернутая_пошаговая_рекомендация_по_найму_и_оптимальной_стратегии_онбординга_и_адаптации_кандидата_в_компании>"\n'
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
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
            "Your task is to conduct a professional SWOT analysis of the candidate relative to the provided vacancy requirements and company context.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain data for a specific SWOT quadrant or bullet point, return an empty array [] for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or technical examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All values in arrays must be written strictly in RUSSIAN.\n"
            "4. Do not limit the number of items in arrays; generate as many objective analytical points as supported by the text.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "strengths": [\n'
            '    "<внутренние_преимущества_кандидата_его_реальные_сильные_стороны_опыт_и_подтвержденные_навыки_релевантные_вакансии>",\n'
            '    "<ключевые_технические_или_управленческие_плюсы_выявленные_из_резюме_и_диалога>"\n'
            '  ],\n'
            '  "weaknesses": [\n'
            '    "<внутренние_недостатки_пробелы_в_компетенциях_или_отсутствие_опыта_в_специфических_сферах_вакансии>",\n'
            '    "<навыки_и_знания_требующие_дополнительного_обучения_или_восстановления_в_процессе_онбординга>"\n'
            '  ],\n'
            '  "opportunities": [\n'
            '    "<внешние_перспективы_и_точки_роста_которые_открываются_для_бизнеса_в_случае_найма_этого_сотрудника>",\n'
            '    "<какие_процессы_цели_или_показатели_компании_кандидат_сможет_объективно_усилить_и_развить>"\n'
            '  ],\n'
            '  "threats": [\n'
            '    "<потенциальные_внешние_риски_и_угрозы_для_бизнеса_связанные_с_возможной_долгой_адаптацией_кандидата>",\n'
            '    "<риски_для_команды_внутренней_атмосферы_или_корпоративной_культуры_исходя_из_управленческого_стиля_кандидата>"\n'
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
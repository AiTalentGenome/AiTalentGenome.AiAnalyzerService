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
            "Your task is to analyze how well the candidate aligns with corporate values based on the provided resume and interview text.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All text values in arrays and strings must be written strictly in RUSSIAN.\n"
            "4. The 'culture_fit_score' must be a dynamically calculated float between 0.0 and 1.0 based on real alignment.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "culture_fit_score": 0.0,\n'
            '  "company_values": [\n'
            '    "<перечисление_ценностей_компании_выявленных_из_текста_вакансии>"\n'
            '  ],\n'
            '  "candidate_opinion": [\n'
            '    "<выявленное_отношение_кандидата_к_рабочим_процессам_контролю_или_корпоративной_этике_на_основе_интервью>"\n'
            '  ],\n'
            '  "alignments": [\n'
            '    "<конкретные_точки_соприкосновения_где_взгляды_кандидата_строго_совпадают_с_ценностями_компании>"\n'
            '  ],\n'
            '  "cultural_risks": [\n'
            '    "<риски_несоответствия_стиля_управления_или_привычек_кандидата_текущей_культуре_и_гибкости_компании>"\n'
            '  ],\n'
            '  "conclusion": "<итоговый_емкий_вывод_о_культурной_совместимости_и_необходимости_поведенческой_адаптации>"\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно парсит и структурирует данные для UI-блока ценностей.
        """
        return {
            "culture_fit_score": float(raw_json.get("culture_fit_score", 0.0)),
            "company_values": list(raw_json.get("company_values", ["командная работа", "порядочность", "честность", "дисциплина"])),
            "candidate_opinion": list(raw_json.get("candidate_opinion", [])),
            "alignments": list(raw_json.get("alignments", [])),
            "cultural_risks": list(raw_json.get("cultural_risks", [])),
            "conclusion": str(raw_json.get("conclusion", ""))
        }
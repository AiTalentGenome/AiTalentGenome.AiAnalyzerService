from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class LeadershipBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Оценка уровня лидерства и командной работы'.
    Входит в родительский блок 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist, Leadership Assessor, and Executive Profiler.\n"
            "Your task is to analyze the candidate's leadership style, team management approaches, and teamwork dynamics based on the provided resume and interview text.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All values in arrays must be written strictly in RUSSIAN.\n"
            "4. Do not limit the number of items in arrays; generate as many as objectively needed.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [\n'
            '    "<анализ_речи_кандидата_его_прямых_высказываний_о_стиле_руководства_и_решении_конфликтов>",\n'
            '    "<конкретные_поведенческие_маркеры_замеченные_в_ходе_диалога_и_интервью>"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "<анализ_структуры_резюме_масштаба_управления_и_количества_подчиненных_если_указано>",\n'
            '    "<описание_специфики_предыдущих_компаний_и_структур_в_которых_развивался_кандидат>"\n'
            '  ],\n'
            '  "conclusion_points": [\n'
            '    "<вывод_о_сформированном_типе_лидерства_структурный_организатор_или_идейный_вдохновитель>",\n'
            '    "<описание_фокуса_в_работе_с_командой_ориентация_на_регламенты_или_на_человеческий_фактор>",\n'
            '    "<оценка_этической_позиции_и_ожиданий_кандидата_от_будущих_подчиненных>"\n'
            '  ]\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает массивы индикаторов лидерского стиля.
        """
        return {
            "interview_manifestation": list(raw_json.get("interview_manifestation", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion_points": list(raw_json.get("conclusion_points", []))
        }
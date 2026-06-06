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
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All values must be written strictly in RUSSIAN.\n"
            "4. Be objective and direct. Highlight boundaries of their skills and constraints clearly based on the data.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "management_style": [\n'
            '    "<особенности_и_характерные_черты_стиля_управления_выявленные_из_опыта_кандидата>",\n'
            '    "<приоритеты_и_ориентация_в_рабочих_процессах_фокус_на_результате_людях_или_регламентах>"\n'
            '  ],\n'
            '  "soft_skills": [\n'
            '    "<оценка_качества_и_стиля_коммуникации_кандидата_на_основе_текста_интервью>",\n'
            '    "<уровень_гибкости_эмпатии_и_адаптивности_в_межличностном_взаимодействии>"\n'
            '  ],\n'
            '  "conclusion": "<итоговый_сжатый_вывод_о_соответствии_управленческих_и_гибких_навыков_кандидата>"\n'
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
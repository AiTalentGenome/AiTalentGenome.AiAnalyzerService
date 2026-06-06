from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class StressToleranceBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Уровень стрессоустойчивости и способность к принятию решений'.
    Входит в родительский блок 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist, Crisis Management Assessor, and Behavioral Profiler.\n"
            "Your task is to analyze the candidate's stress tolerance, emotional stability, and decision-making patterns based on the provided resume and interview text.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All values in arrays must be written strictly in RUSSIAN.\n"
            "4. Do not limit the number of items in arrays; generate as many analytical bullet points as objectively supported by the source text.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [\n'
            '    "<анализ_эмоционального_контроля_и_поведения_кандидата_при_ответах_на_сложные_или_неудобные_вопросы>",\n'
            '    "<описание_того_как_кандидат_описывает_свой_опыт_справления_с_кризисными_ситуациями>"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "<выявление_индикаторов_напряженной_рабочей_среды_высокой_ответственности_или_сжатых_сроков_в_карьерном_пути>",\n'
            '    "<оценка_сложности_и_масштаба_предыдущих_задач_требовавших_повышенной_психологической_устойчивости>"\n'
            '  ],\n'
            '  "conclusion_points": [\n'
            '    "<определение_психологического_типа_устойчивости_и_уровня_контроля_эмоций>",\n'
            '    "<анализ_стиля_принятия_решений_степень_рациональности_логики_или_импульсивности_в_кризисе>",\n'
            '    "<итоговый_управленческий_вектор_поведения_в_конфликтной_или_стрессовой_ситуации>"\n'
            '  ]\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает массивы поведенческих индикаторов стрессоустойчивости.
        """
        return {
            "interview_manifestation": list(raw_json.get("interview_manifestation", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion_points": list(raw_json.get("conclusion_points", []))
        }
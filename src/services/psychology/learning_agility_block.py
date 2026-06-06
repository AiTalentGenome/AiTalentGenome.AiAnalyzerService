from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class LearningAgilityBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Склонность к обучению и развитию'.
    Входит в родительский блок 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist, Corporate Trainer, and Learning Agility Assessor.\n"
            "Your task is to analyze the candidate's learning agility, adaptability, and openness to new knowledge based on the provided resume and interview text.\n\n"
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
            '    "<анализ_высказываний_кандидата_в_интервью_отражающих_его_реальную_готовность_к_обучению>",\n'
            '    "<отношение_кандидата_к_выявленным_пробелам_в_знаниях_и_его_реакция_на_необходимость_развития>"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "<маркеры_адаптивности_из_карьерного_пути_смена_сфер_переходы_на_новые_уровни_управления>",\n'
            '    "<факты_освоения_новых_инструментов_технологий_или_методологий_на_предыдущих_местах_работы>"\n'
            '  ],\n'
            '  "conclusion_points": [\n'
            '    "<итоговый_вывод_о_прагматике_обучения_соотношение_теоретического_интереса_и_практической_пользы_для_бизнеса>",\n'
            '    "<прогноз_скорости_адаптации_сотрудника_при_входе_в_новые_рабочие_процессы>",\n'
            '    "<оценка_базовой_внутренней_позиции_кандидата_по_отношению_к_непрерывному_развитию>"\n'
            '  ]\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает массивы индикаторов обучаемости и адаптивности.
        """
        return {
            "interview_manifestation": list(raw_json.get("interview_manifestation", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion_points": list(raw_json.get("conclusion_points", []))
        }
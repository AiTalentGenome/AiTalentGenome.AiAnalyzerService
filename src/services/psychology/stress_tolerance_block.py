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
            "Your task is to analyze the candidate's stress tolerance, emotional stability, and decision-making patterns based on their resume and interview text.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullet points, and descriptions must be strictly in RUSSIAN.\n"
            "3. Do not limit the number of bullet points; generate as many as objectively needed based on the text context.\n"
            "4. Focus on emotional control, response to crisis situations, and the logic of decision-making (rational vs. impulsive).\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [\n'
            '    "Как проявляется в интервью (например: Держится спокойно, рассматривает стресс как рабочий процесс)",\n'
            '    "Реакция на сложные вопросы (например: На вопросы о кризисах отвечает структурно, предлагает поэтапные решения)"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "Как проявляется в резюме (например: Опыт работы в сложных проектах с жестким контролем сроков)",\n'
            '    "Индикаторы среды (например: Работал в напряжённых условиях: ремонты, управление большими коллективами)"\n'
            '  ],\n'
            '  "conclusion_points": [\n'
            '    "Психологический тип устойчивости (например: Стрессоустойчивый, хладнокровный, структурный)",\n'
            '    "Стиль принятия решений (например: Принимает решения логично, без импульсивности)",\n'
            '    "Управленческий вектор (например: Скорее кризисный управленец, чем гибкий дипломат – ориентирован на порядок)"\n'
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
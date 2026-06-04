from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class MotivationBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Оценка мотивации и профессиональной самооценки'.
    Входит в родительский блок 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist, Behavioral Interviewer, and Talent Assessor.\n"
            "Your task is to analyze the candidate's motivation matrix and professional self-esteem based on their resume and interview text.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullet points, and descriptions must be strictly in RUSSIAN.\n"
            "3. Do not limit the number of bullet points; generate as many as objectively needed based on the context.\n"
            "4. Be precise in evaluating self-esteem (e.g., adequate, overinflated, defensive) and core motivational drivers.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [\n'
            '    "Как проявляется в интервью (например: Чётко обозначил зарплатные ожидания – ориентирован на достойный уровень оплаты)",\n'
            '    "Мотивационный маркер (например: Мотивация построена на дисциплине, порядке, организации процессов)"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "Как проявляется в резюме (например: Нет частых смен работы, всегда занимал ответственные позиции)",\n'
            '    "Индикатор самооценки (например: Самооценка уверенная, но без перегибов – чётко знает свою ценность)"\n'
            '  ],\n'
            '  "conclusion_points": [\n'
            '    "Вывод по мотивации (например: Мотивация основана на стабильности, чёткости процессов)",\n'
            '    "Вывод по самооценке (например: Самооценка адекватная – понимает свою ценность)",\n'
            '    "Условия вовлеченности (например: Заинтересован в работе, если сможет реально влиять на процессы)"\n'
            '  ]\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает массивы манифестации мотивации и самооценки кандидатов.
        """
        return {
            "interview_manifestation": list(raw_json.get("interview_manifestation", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion_points": list(raw_json.get("conclusion_points", []))
        }
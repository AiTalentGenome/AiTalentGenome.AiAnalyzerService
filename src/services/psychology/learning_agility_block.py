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
            "Your task is to analyze the candidate's learning agility, adaptability, and openness to new knowledge based on their resume and interview text.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullet points, and descriptions must be strictly in RUSSIAN.\n"
            "3. Do not limit the number of bullet points; generate as many as objectively needed based on the text context.\n"
            "4. Clearly distinguish between theoretical learning (learning for the sake of interest) and pragmatic/practical learning (learning for a specific task).\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [\n'
            '    "Как проявляется в интервью (например: Готов учиться, но только если видит в этом практическую пользу)",\n'
            '    "Отношение к пробелам в знаниях (например: Осознаёт, что специфические навыки требуют восстановления, и готов практиковаться)"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "Как проявляется в резюме (например: Работал на разных уровнях управления, что говорит о способности адаптироваться)",\n'
            '    "Освоение технологий (например: Изучал новые инструменты и технологии, если это входило в его прямые обязанности)"\n'
            '  ],\n'
            '  "conclusion_points": [\n'
            '    "Прагматика обучения (например: Готов учиться, но не тратит время на теорию – важен практический смысл)",\n'
            '    "Скорость адаптации (например: Навыки сможет восстановить непосредственно в работе, потребуется небольшая адаптация)",\n'
            '    "Базовая позиция к развитию (например: Не фанат абстрактных знаний, но если это необходимо для бизнеса – изучит и применит)"\n'
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
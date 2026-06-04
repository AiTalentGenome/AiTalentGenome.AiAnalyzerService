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
            "Your task is to analyze the candidate's leadership style, team management approaches, and teamwork dynamics based on their resume and interview text.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullet points, and descriptions must be strictly in RUSSIAN.\n"
            "3. Do not limit the number of bullet points; generate as many as objectively needed based on the text context.\n"
            "4. Differentiate clearly between emotional leaders (inspirers) and structural leaders (organizers/planners).\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [\n'
            '    "Как проявляется в интервью (например: Лидер-организатор, а не эмоциональный вдохновитель)",\n'
            '    "Управленческий подход (например: В конфликтных ситуациях предлагает решения через регламент и субординацию)"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "Как проявляется в резюме (например: Управлял коллективами от 15 до 160 человек)",\n'
            '    "Контекст управления (например: Привык работать в структурах, где важна система и строгая дисциплина)"\n'
            '  ],\n'
            '  "conclusion_points": [\n'
            '    "Тип лидерства (например: Лидер-организатор, а не харизматичный вдохновитель)",\n'
            '    "Ориентация в команде (например: Ориентирован на порядок, исполнение, чёткие обязанности)",\n'
            '    "Этическая позиция (например: Требователен к коллективу, но честен и справедлив)"\n'
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
from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class PsychologicalVerdictBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Вывод по психологической оценке кандидата'.
    Финальный агрегирующий блок вкладки 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are a Senior Executive Coach, Chief HR Officer, and Lead Corporate Profiler.\n"
            "Your task is to generate the final psychological verdict, summary, strengths, risks, and actionable recommendations based on all previous psychological insights, resume, and interview texts.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullet points, and descriptions must be strictly in RUSSIAN.\n"
            "3. Do not limit the number of bullet points in lists; generate as many as objectively supported by the data.\n"
            "4. Provide realistic, balanced recommendations considering both the pros and cons of the candidate's personality type.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "general_verdict": "Общее развернутое заключение по психологической оценке кандидата (его потенциал, сильные стороны, условия успешной адаптации).",\n'
            '  "strengths": [\n'
            '    "Ключевая психологическая сильная сторона (например: Высокая стрессоустойчивость, холодный разум, структурность)",\n'
            '    "Управленческий плюс (например: Богатый опыт контроля дисциплины, процессов и ресурсов)"\n'
            '  ],\n'
            '  "things_to_consider": [\n'
            '    "Что необходимо учитывать / Зоны риска (например: Строгий стиль управления – важно, чтобы коллектив был готов)",\n'
            '    "Технический/поведенческий нюанс (например: Навык работы со специфическими инструментами/чертежами требует восстановления)"\n'
            '  ],\n'
            '  "recommendations": [\n'
            '    "Сценарий успешного найма (например: Если компании нужен системный управленец-порядочник – это отличный выбор)",\n'
            '    "Предостережение (например: Если в команде ожидается мягкий, дипломатичный стиль – кандидат может показаться слишком строгим)"\n'
            '  ]\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает финальные вердикты, списки сильных сторон, рисков и рекомендаций.
        """
        return {
            "general_verdict": str(raw_json.get("general_verdict", "")),
            "strengths": list(raw_json.get("strengths", [])),
            "things_to_consider": list(raw_json.get("things_to_consider", [])),
            "recommendations": list(raw_json.get("recommendations", []))
        }
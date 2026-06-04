from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class PsychologicalProfileBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Общий психологический профиль'.
    Входит в родительский блок 'Психологический портрет'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert Forensic Psychologist and Executive Behavioral Analyst.\n"
            "Your task is to compile a general psychological profile of the candidate based on their interview transcript and resume structure.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, bullet points, and conclusions must be strictly in RUSSIAN.\n"
            "3. Analyze communication style deeply: notice if speech is fact-driven, authoritative, structured, or fluid.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "key_observations": [\n'
            '    "Ключевое наблюдение (например: Уверенная, собранная речь, говорит чётко, без пауз)",\n'
            '    "Концентрация на сути (например: Не использует лишних слов, даёт конкретные факты)"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "Как проявляется в резюме (например: Чёткая структура, перечисление конкретных задач)",\n'
            '    "Прагматичный подход (например: Мало про личные достижения, акцент на стабильность)"\n'
            '  ],\n'
            '  "conclusion": "Итоговый психологический вывод (например: Кандидат – структурный, дисциплинированный, уверенный в себе управленец)"\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно извлекает списки наблюдений и финальный вердикт профиля.
        """
        return {
            "key_observations": list(raw_json.get("key_observations", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion": str(raw_json.get("conclusion", ""))
        }
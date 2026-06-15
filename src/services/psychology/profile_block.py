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
            "Your task is to compile a general psychological profile of the candidate based ONLY on the verified data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract real behavioral and structural facts strictly from the <candidate_resume> and <candidate_cover_letter> tags.\n"
            "2. Do not assume, guess, or extrapolate character traits. If factual communication markers are missing, return empty arrays or strings.\n"
            "3. NEVER reuse, echo, or rewrite any words, instructions, or keys from this system prompt in your JSON output fields.\n"
            "4. THIRD PERSON RULE: Strictly write all descriptions in the THIRD PERSON (e.g., 'Кандидат демонстрирует', 'Сотрудник ориентирован'). Writing from the first person ('Я', 'Мой опыт') is STRICTLY FORBIDDEN.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All text values, summary points, and conclusions inside the JSON must be written strictly in RUSSIAN.\n"
            "4. Avoid nested arrays; output a clean, flat list of strings for array keys.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "key_observations": [],\n'  # Полностью очистили от текста-подсказок, чтобы Qwen не зеркалил ТЗ
            '  "resume_manifestation": [],\n'
            '  "conclusion": ""\n'
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
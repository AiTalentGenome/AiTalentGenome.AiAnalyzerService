from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class LearningAgilityBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Склонность к обучению и развитию (Learning Agility)'.
    Оптимизирован под Qwen 2.5 14B с защитой от ленивой генерации.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist, Corporate Trainer, and Learning Agility Assessor.\n"
            "Your task is to analyze the candidate's learning agility, adaptability, and openness to new knowledge based on the provided resume and interview text.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n"
            "4. THIRD PERSON RULE: Strictly write all descriptions in the THIRD PERSON (e.g., 'Кандидат готов развиваться', 'Прогноз адаптации сотрудника'). Writing from the first person is STRICTLY FORBIDDEN.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All values in arrays must be written strictly in RUSSIAN.\n"
            "4. Avoid nested arrays; output a flat list of strings for each key.\n"
            "5. CONTENT REQUIREMENT FOR ARRAYS:\n"
            "   - For 'interview_manifestation': Generate fully finished sentences analyzing the candidate's explicit statements regarding willingness to study and their reaction to existing knowledge gaps.\n"
            "   - For 'resume_manifestation': Generate fully finished sentences tracking career adaptability markers (domain changes, shifts in roles) and facts of mastering new tools or software.\n"
            "   - For 'conclusion_points': Generate exactly three clear analytical sentences outlining: 1) pragmatics of learning (theory vs practical business value), 2) a precise onboarding adaptation speed forecast, 3) the candidate's core internal stance toward continuous self-development.\n"
            "   NEVER output short broken phrases, raw templates, or placeholder fragments.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "interview_manifestation": [],\n'
            '  "resume_manifestation": [],\n'
            '  "conclusion_points": []\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "interview_manifestation": list(raw_json.get("interview_manifestation", [])),
            "resume_manifestation": list(raw_json.get("resume_manifestation", [])),
            "conclusion_points": list(raw_json.get("conclusion_points", []))
        }
from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class LeadershipBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Оценка уровня лидерства и командной работы'.
    Оптимизирован под Qwen 2.5 14B с защитой от ленивой генерации.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist, Leadership Assessor, and Executive Profiler.\n"
            "Your task is to analyze the candidate's leadership style, team management approaches, and teamwork dynamics based ONLY on the verified data inside the provided XML tags.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Extract real facts strictly from the <candidate_resume> and <candidate_cover_letter> tags. Do not assume or extrapolate management scale.\n"
            "2. If the text does not contain clear indicators for leadership or team size (e.g., candidate is an individual contributor), explicitly state this in the arrays instead of inventing numbers.\n"
            "3. NEVER reuse, echo, or rewrite phrases or concepts listed in these system instructions in your JSON output.\n"
            "4. THIRD PERSON RULE: Write everything exclusively in the third person ('Кандидат ориентирован', 'В опыте сотрудника'). First person ('Я', 'Мой') is strictly forbidden.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All elements inside arrays must be written strictly in RUSSIAN.\n"
            "4. Avoid nested arrays; output a clean, flat list of strings for each array key.\n"
            "5. CONTENT REQUIREMENT FOR ARRAYS:\n"
            "   - For 'interview_manifestation': Generate fully finished sentences analyzing the candidate's speech markers, communication style, and direct statements about leadership or conflict resolution.\n"
            "   - For 'resume_manifestation': Generate fully finished sentences detailing management scale, team size, and organizational structures extracted from their career history.\n"
            "   - For 'conclusion_points': Generate exactly three clear analytical conclusions detailing: 1) the established leadership type (structural organizer or ideological leader), 2) focus on regulations vs human factor, 3) ethical expectations from future subordinates.\n"
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
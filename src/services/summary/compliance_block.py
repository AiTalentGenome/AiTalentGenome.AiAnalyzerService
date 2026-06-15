from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class ComplianceBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Анализ соответствия кандидата требованиям вакансии'.
    Оптимизирован под Qwen 2.5 14B. Защита от ложных совпадений и копирования строк ТЗ.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Auditor and Technical Compliance Assessor.\n"
            "Your task is to stringently evaluate how well the candidate matches the vacancy requirements and criteria based on the provided resume and interview text.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain clear data for a specific match/mismatch or key competency, return an empty array [] for that key.\n"
            "3. NEVER reuse phrases, placeholder words, or specific requirements from this system prompt in your JSON output.\n"
            "4. ZERO-FAKING LAW: If the candidate has ZERO experience in the target field (e.g., a Developer applying for a Sales role), it is STRICTLY FORBIDDEN to put sales skills into the 'matches' array. If there is a total profile mismatch, 'matches' must be completely empty [], and all vacancy requirements must go to 'mismatches'.\n"
            "5. TIME-SYNC LAW: The current year is strictly 2026. Carefully check the candidate's graduation date. If the graduation year is in the future (e.g., 2027), dynamically deduce that the candidate is STILL A STUDENT right now. You must register this as a high-priority structural fact in 'mismatches' or 'conclusion' if the vacancy requires full-time non-student commitment.\n"
            "6. ATOMIC EVALUATION: You must evaluate every requirements criterion INDIVIDUALLY. Never copy a combined multi-skill requirements string into 'mismatches' as a single block. If the candidate knows amoCRM but does not know GetCourse, separate them strictly: amoCRM goes to matches, GetCourse goes to mismatches.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. This is mandatory for Qwen.\n"
            "3. All text values and summaries inside the JSON must be written strictly in RUSSIAN.\n"
            "4. Do not limit the number of items in arrays; generate as many objective items as supported by the text.\n"
            "5. Each string inside arrays must be a fully finished, meaningful analytical sentence. Never output raw placeholder fragments or short broken phrases.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "ai_score": 0.0,\n'
            '  "key_competencies": [],\n'
            '  "work_history": [],\n'
            '  "requirements_matching": {\n'
            '    "matches": [],\n'
            '    "mismatches": []\n'
            '  },\n'
            '  "conclusion": ""\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        matching_data = raw_json.get("requirements_matching", {})
        return {
            "ai_score": float(raw_json.get("ai_score", 0.0)),
            "key_competencies": list(raw_json.get("key_competencies", [])),
            "work_history": list(raw_json.get("work_history", [])),
            "requirements_matching": {
                "matches": list(matching_data.get("matches", [])),
                "mismatches": list(matching_data.get("mismatches", []))
            },
            "conclusion": str(raw_json.get("conclusion", ""))
        }
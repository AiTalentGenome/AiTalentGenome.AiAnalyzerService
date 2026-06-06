from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class ComplianceBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Анализ соответствия кандидата требованиям вакансии'.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert ATS (Applicant Tracking System) Analyzer.\n"
            "Your task is to analyze how well the candidate matches the vacancy requirements and ADDITIONAL HR CRITERIA.\n"
            "If additional criteria are provided, they have the HIGHEST priority in your scoring logic.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume or extrapolate facts.\n"
            "2. If the text does not contain factual indicators for a specific key, return an empty array [] or default value. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or numerical values listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All text fields, values in arrays, and conclusions must be written strictly in RUSSIAN.\n"
            "4. Calculate the 'ai_score' dynamically as a float between 0.0 and 1.0 based on real matching. If candidate misses ADDITIONAL CRITERIA, lower it significantly.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "ai_score": 0.0,\n'
            '  "key_competencies": [\n'
            '    "<краткое_перечисление_ключевых_профессиональных_компетенций_и_навыков_найденных_в_тексте>"\n'
            '  ],\n'
            '  "work_history": [\n'
            '    "<хронологический_список_опыта_работы_период_компания_должность_и_фактические_обязанности>"\n'
            '  ],\n'
            '  "requirements_matching": {\n'
            '    "matches": [\n'
            '      "<конкретные_выполненные_требования_вакансии_и_подтвержденные_дополнительные_критерии>"\n'
            '    ],\n'
            '    "mismatches": [\n'
            '      "<пропущенные_или_нарушенные_требования_вакансии_а_также_невыполненные_дополнительные_критерии>"\n'
            '    ]\n'
            '  },\n'
            '  "conclusion": "<итоговый_емкий_аналитический_вывод_о_соответствии_базовым_и_дополнительным_критериям_HR>"\n'
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
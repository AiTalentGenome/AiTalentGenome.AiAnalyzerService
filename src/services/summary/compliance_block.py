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
            "Your task is to analyze how well the candidate matches the vacancy requirements and ADDITIONAL HR CRITERA.\n"
            "If additional criteria are provided, they have the HIGHEST priority in your scoring logic.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text descriptions, fields, and arrays must be written in RUSSIAN.\n"
            "3. Be specific and objective. Check if additional criteria are fully satisfied.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "ai_score": 0.85,\n' # Calculate this score strictly. If candidate misses ADDITIONAL CRITERIA, lower it significantly.
            '  "key_competencies": ["Краткое саммари ключевого опыта и образования кандидата"],\n'
            '  "work_history": [\n'
            '    "Название компании (Год - Год) — Должность (ключевые зоны ответственности)"\n'
            '  ],\n'
            '  "requirements_matching": {\n'
            '    "matches": ["В чем кандидат точно силен и какие требования/критерии выполнены"],\n'
            '    "mismatches": ["Какие требования вакансии или ДОПОЛНИТЕЛЬНЫЕ КРИТЕРИИ пропущены или нарушены"]\n'
            '  },\n'
            '  "conclusion": "Итоговый емкий вывод с учетом соответствия базовым и дополнительным критериям."\n'
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
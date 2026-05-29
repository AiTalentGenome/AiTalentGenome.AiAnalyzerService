from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class CultureFitBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Анализ ценностного совпадения'.
    Входит в родительский блок 'Общая сводка' и оценивает Culture Fit.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Corporate Culture Analyst.\n"
            "Your task is to analyze how well the candidate aligns with corporate values (e.g., командная работа, порядочность, честность, дисциплина) and identify management style risks.\n\n"
            "CRITICAL RULES:\n"
            "1. You must output ONLY a valid JSON object matching the JSON SCHEMA below.\n"
            "2. All text values, matching items, and descriptions must be strictly in RUSSIAN.\n"
            "3. Be objective. If the candidate prefers a strict or rigid management style, explicitly list it as a risk if the company values flexibility.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "culture_fit_score": 0.80,\n' # Float value between 0.0 and 1.0 representing alignment
            '  "company_values": ["командная работа", "порядочность", "честность", "дисциплина"],\n'
            '  "candidate_opinion": [\n'
            '    "Что думает кандидат (например: Считает, что жесткий контроль и дисциплина – ключ к эффективной работе)"\n'
            '  ],\n'
            '  "alignments": [\n'
            '    "Конкретные совпадения (например: Дисциплина и ответственность – полностью соответствуют ценностям компании)"\n'
            '  ],\n'
            '  "cultural_risks": [\n'
            '    "Риски (например: Привык к более жесткому стилю управления, что может вызывать сопротивление)"\n'
            '  ],\n'
            '  "conclusion": "Итоговый вывод (например: Кандидат совпадает по ключевым ценностям, но его стиль может потребовать адаптации)"\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Безопасно парсит и структурирует данные для UI-блока ценностей.
        """
        return {
            "culture_fit_score": float(raw_json.get("culture_fit_score", 0.0)),
            "company_values": list(raw_json.get("company_values", ["командная работа", "порядочность", "честность", "дисциплина"])),
            "candidate_opinion": list(raw_json.get("candidate_opinion", [])),
            "alignments": list(raw_json.get("alignments", [])),
            "cultural_risks": list(raw_json.get("cultural_risks", [])),
            "conclusion": str(raw_json.get("conclusion", ""))
        }
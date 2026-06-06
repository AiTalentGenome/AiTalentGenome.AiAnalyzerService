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
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] for that key. Do not invent details.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All values in arrays and strings must be written strictly in RUSSIAN.\n"
            "4. Do not limit the number of items in arrays; generate as many analytical bullet points as objectively supported by the source text.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "general_verdict": "<интегрированное_развернутое_психологическое_заключение_о_соответствии_личности_кандидата_и_условиях_его_адаптации>",\n'
            '  "strengths": [\n'
            '    "<доминирующая_психологическая_сильная_сторона_выявленная_на_основе_анализа>",\n'
            '    "<управленческие_или_поведенческие_плюсы_проявившиеся_в_опыте_и_интервью>"\n'
            '  ],\n'
            '  "things_to_consider": [\n'
            '    "<критические_психологические_риски_или_особенности_поведения_на_которые_стоить_обратить_внимание>",\n'
            '    "<возможные_точки_сопротивления_или_барьеры_в_коммуникации_и_стиле_менеджмента>"\n'
            '  ],\n'
            '  "recommendations": [\n'
            '    "<рекомендация_по_оптимальному_сценарию_интеграции_сотрудника_в_существующую_команду>",\n'
            '    "<совет_для_высшего_руководства_по_эффективному_взаимодействию_и_удержанию_данного_человека>"\n'
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
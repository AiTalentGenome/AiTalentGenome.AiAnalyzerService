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
            "Your task is to compile a general psychological profile of the candidate based on the provided interview transcript and resume structure.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual text provided in the user prompt. Do not assume, guess, or extrapolate facts.\n"
            "2. If the text does not contain indicators for a specific key, return an empty array [] or empty string for that key.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt in your JSON output.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a raw, valid JSON object matching the JSON SCHEMA below.\n"
            "2. Do not wrap the response in markdown blocks like triple backticks JSON. Output pure JSON.\n"
            "3. All values and conclusions must be written strictly in RUSSIAN.\n"
            "4. Analyze communication style deeply: notice if speech is fact-driven, authoritative, structured, or fluid.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "key_observations": [\n'
            '    "<описание_стиля_коммуникации_скорости_речи_и_поведения_на_основе_текста_интервью>",\n'
            '    "<маркеры_фокусировки_на_фактах_структурированности_мышления_и_эмоционального_контроля>"\n'
            '  ],\n'
            '  "resume_manifestation": [\n'
            '    "<анализ_особенностей_оформления_резюме_соблюдения_хронологии_и_распределения_акцентов>",\n'
            '    "<оценка_прагматичности_текста_соотношение_описания_процессов_и_личных_достижений>"\n'
            '  ],\n'
            '  "conclusion": "<итоговый_емкий_психологический_вывод_о_базовом_психотипе_личностных_установках_и_стиле_мышления_кандидата>"\n'
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
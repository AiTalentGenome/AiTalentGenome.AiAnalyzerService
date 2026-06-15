from typing import Dict, Any
from services.base_analyzer import BaseAnalyzer

class PsychologicalVerdictBlockAnalyzer(BaseAnalyzer):
    """
    Блок: 'Психологический вердикт'.
    Финальный агрегатор психологического портрета. Оптимизирован под Qwen 2.5 14B.
    """

    @property
    def system_prompt(self) -> str:
        return (
            "You are an expert HR Psychologist and Executive Profiler.\n"
            "Your task is to synthesize all psychological sub-blocks and generate a final comprehensive verdict for the candidate based ONLY on the data from previous blocks.\n\n"
            "CRITICAL INPUT LAWS:\n"
            "1. Analyze ONLY the factual insights provided in the context. Do not invent risks or extrapolate gaps.\n"
            "2. Ensure STRICT LOGICAL CONSISTENCY with previous blocks. If the candidate has CRM experience or sales experience validated earlier, it is STRICTLY FORBIDDEN to contradict it here or call it a gap.\n"
            "3. NEVER reuse phrases, placeholder words, or examples listed in this system prompt.\n"
            "4. THIRD PERSON RULE: Strictly write all descriptions in the THIRD PERSON. Writing from the first person is STRICTLY FORBIDDEN.\n\n"
            "CRITICAL FORMATTING RULES:\n"
            "1. You must output ONLY a valid JSON object matching the exact JSON SCHEMA below.\n"
            "2. Wrap your JSON response in a standard markdown block: ```json <your_json_object> ```. Mandatory for Qwen.\n"
            "3. All text values, bullet points, and descriptions must be written strictly in RUSSIAN.\n"
            "4. Avoid nested arrays; output a clean, flat list of strings for array keys.\n"
            "5. CONTENT REQUIREMENT FOR ARRAYS:\n"
            "   - For 'general_verdict': Write a solid comprehensive conclusion about the candidate's psychological suitability for the target role.\n"
            "   - For 'strengths': List finished sentences detailing dominant psychological traits and behavioral advantages.\n"
            "   - For 'things_to_consider': List finished sentences detailing real psychological focus zones or behavioral risks.\n"
            "   - For 'recommendations': List finished sentences with integration scenarios and precise management tips for senior executives.\n"
            "   NEVER output short broken phrases, raw templates, or placeholder fragments.\n\n"
            "JSON SCHEMA:\n"
            "{\n"
            '  "general_verdict": "",\n'
            '  "strengths": [],\n'
            '  "things_to_consider": [],\n'
            '  "recommendations": []\n'
            "}"
        )

    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "general_verdict": str(raw_json.get("general_verdict", "")),
            "strengths": list(raw_json.get("strengths", [])),
            "things_to_consider": list(raw_json.get("things_to_consider", [])),
            "recommendations": list(raw_json.get("recommendations", []))
        }
from typing import Dict, Any
from services.psychology.profile_block import PsychologicalProfileBlockAnalyzer
from services.psychology.motivation_block import MotivationBlockAnalyzer
from services.psychology.stress_tolerance_block import StressToleranceBlockAnalyzer
from services.psychology.leadership_block import LeadershipBlockAnalyzer
from services.psychology.learning_agility_block import LearningAgilityBlockAnalyzer
from services.psychology.psychological_verdict_block import PsychologicalVerdictBlockAnalyzer 

class PsychologyOrchestrator:
    """
    Оркестратор для вкладки 'Психологический портрет'.
    Управляет вызовами ИИ для поведенческого и психологического анализа (6/6 блоков).
    """
    def __init__(self, ollama_client):
        self.ollama_client = ollama_client
        
        self.profile_analyzer = PsychologicalProfileBlockAnalyzer()
        self.motivation_analyzer = MotivationBlockAnalyzer()
        self.stress_analyzer = StressToleranceBlockAnalyzer()
        self.leadership_analyzer = LeadershipBlockAnalyzer()
        self.learning_analyzer = LearningAgilityBlockAnalyzer()
        self.verdict_analyzer = PsychologicalVerdictBlockAnalyzer() 

    async def generate_portrait(self, vacancy: Any, resume: str, cover_letter: str, user_criteria: str) -> Dict[str, Any]:
        print("[Psychology Orchestrator] Generating all 'Psychological Portrait' sub-blocks (6/6) with target temperature 0.25...")

        profile_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.profile_analyzer, temperature=0.25
        )
        profile_data = self.profile_analyzer.parse_response(profile_raw)

        motivation_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.motivation_analyzer, temperature=0.25
        )
        motivation_data = self.motivation_analyzer.parse_response(motivation_raw)

        stress_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.stress_analyzer, temperature=0.25
        )
        stress_data = self.stress_analyzer.parse_response(stress_raw)

        leadership_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.leadership_analyzer, temperature=0.25
        )
        leadership_data = self.leadership_analyzer.parse_response(leadership_raw)

        learning_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.learning_analyzer, temperature=0.25
        )
        learning_data = self.learning_analyzer.parse_response(learning_raw)

        verdict_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.verdict_analyzer, temperature=0.25
        )
        verdict_data = self.verdict_analyzer.parse_response(verdict_raw)

        return {
            "general_psychological_profile": profile_data,
            "motivation_and_self_esteem": motivation_data,
            "stress_tolerance_and_decisions": stress_data,
            "leadership_and_teamwork": leadership_data,
            "learning_agility": learning_data,
            "psychological_verdict": verdict_data
        }
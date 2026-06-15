from typing import Dict, Any
from services.summary.compliance_block import ComplianceBlockAnalyzer
from services.summary.summary_block import SummaryBlockAnalyzer
from services.summary.culture_fit_block import CultureFitBlockAnalyzer
from services.summary.management_style_block import ManagementStyleBlockAnalyzer
from services.summary.swot_block import SwotBlockAnalyzer
from services.summary.final_verdict_block import FinalVerdictBlockAnalyzer # Добавили импорт!

class SummaryOrchestrator:
    """
    Оркестратор для вкладки 'Общая сводка'.
    Управляет вызовами и агрегацией всех подблоков этой группы.
    """
    def __init__(self, ollama_client):
        self.ollama_client = ollama_client
        
        self.compliance_analyzer = ComplianceBlockAnalyzer()
        self.summary_block_analyzer = SummaryBlockAnalyzer()
        self.culture_fit_analyzer = CultureFitBlockAnalyzer()
        self.management_analyzer = ManagementStyleBlockAnalyzer()
        self.swot_analyzer = SwotBlockAnalyzer()
        self.final_verdict_analyzer = FinalVerdictBlockAnalyzer() 

    async def generate_summary(self, vacancy: Any, resume: str, cover_letter: str, user_criteria: str) -> Dict[str, Any]:
        print("[Summary Orchestrator] Generating all 'General Summary' sub-blocks (6/6)...")
        
        compliance_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.compliance_analyzer
        )
        compliance_data = self.compliance_analyzer.parse_response(compliance_raw)
        
        summary_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.summary_block_analyzer
        )
        summary_data = self.summary_block_analyzer.parse_response(summary_raw)
        
        culture_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.culture_fit_analyzer
        )
        culture_data = self.culture_fit_analyzer.parse_response(culture_raw)
        
        management_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.management_analyzer
        )
        management_data = self.management_analyzer.parse_response(management_raw)

        swot_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.swot_analyzer
        )
        swot_data = self.swot_analyzer.parse_response(swot_raw)

        verdict_raw = await self.ollama_client.execute_block(
            vacancy=vacancy, resume=resume, cover_letter=cover_letter, user_criteria=user_criteria, analyzer=self.final_verdict_analyzer
        )
        verdict_data = self.final_verdict_analyzer.parse_response(verdict_raw)
        
        return {
            "compliance_analysis": compliance_data,
            "brief_summary": summary_data,
            "culture_fit_analysis": culture_data,
            "management_and_soft_skills": management_data,
            "swot_analysis": swot_data,
            "final_verdict": verdict_data
        }
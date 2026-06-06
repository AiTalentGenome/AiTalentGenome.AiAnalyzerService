import json
import asyncio
import re  # Добавили для продвинутой очистки строк
from typing import Dict, Any, List, Tuple
from ollama import Client
from services.summary_orchestrator import SummaryOrchestrator
from services.psychology_orchestrator import PsychologyOrchestrator
from services.base_analyzer import BaseAnalyzer

class MainAnalysisOrchestrator:
    def __init__(self, model_name: str = "llama3:latest"):
        self.model_name = model_name
        self.ollama_client = Client()
        self.summary_orch = SummaryOrchestrator(self)
        self.psychology_orch = PsychologyOrchestrator(self)

    @staticmethod
    def _call_ollama(client: Client, model: str, system: str, prompt: str) -> Any:
        return client.generate(
            model=model,
            system=system,
            prompt=prompt,
            format="json",
            options={
                "temperature": 0.1,
                "num_predict": 2048
            }
        )

    async def execute_block(self, vacancy: Any, resume: str, cover_letter: str, user_criteria: str, analyzer: BaseAnalyzer) -> Dict[str, Any]:
        skills_str = ", ".join(vacancy.key_skills) if vacancy.key_skills else "Не указаны"

        # ЗАЩИТА 1: Проверяем, что входные данные не пустые, иначе ИИ начнет выдумывать факты
        resume_clean = resume.strip() if resume else "Информация о резюме отсутствует."
        cover_clean = cover_letter.strip() if cover_letter else "Сопроводительное письмо отсутствует."

        print("\n" + "="*80)
        print(f"[DATA CHECK] Incoming data for analyzer: '{analyzer.__class__.__name__}'")
        print(f" -> Vacancy Title: {vacancy.title}")
        print(f" -> User Criteria Length: {len(user_criteria) if user_criteria else 0} chars")
        print(f" -> Resume Raw Length: {len(resume) if resume else 0} chars")
        print(f" -> Cover Letter Raw Length: {len(cover_letter) if cover_letter else 0} chars")

        # Выводим превью данных для визуального контроля
        print("-" * 50)
        print(f" -> Resume Preview: {resume_clean[:150]}...")
        print(f" -> Cover Preview: {cover_clean[:150]}...")
        print("="*80 + "\n")

        vacancy_context = (
            f"=== ТРЕБОВАНИЯ ВАКАНСИИ ===\n"
            f"Название должности: {vacancy.title}\n"
            f"Опыт работы: {vacancy.experience}\n"
            f"Ключевые навыки (Key Skills): {skills_str}\n"
            f"Описание обязанностей и условий:\n{vacancy.description}\n"
        )

        criteria_context = ""
        if user_criteria and user_criteria.strip():
            criteria_context = f"=== КРИТИЧЕСКИЕ КРИТЕРИИ ОТ HR (ПРИОРИТЕТ) ===\n{user_criteria}\n\n"

        user_content = (
            f"{criteria_context}"
            f"{vacancy_context}\n"
            f"=== КАНДИДАТ: ТЕКСТ РЕЗЮМЕ ===\n{resume_clean}\n\n"
            f"=== КАНДИДАТ: СОПРОВОДИТЕЛЬНОЕ ПИСЬМО ===\n{cover_clean}\n"
        )

        try:
            print(f"[Ollama] Running sub-block analysis: '{analyzer.__class__.__name__}'...")

            response = await asyncio.to_thread(
                self._call_ollama,
                self.ollama_client,
                self.model_name,
                analyzer.system_prompt,
                user_content
            )

            raw_text = response.get("response", "{}").strip()

            # ЗАЩИТА 2: Улучшенная очистка от Markdown (решает проблему, если модель ставит пробелы перед кавычками)
            raw_text = re.sub(r'^```json\s*', '', raw_text, flags=re.IGNORECASE)
            raw_text = re.sub(r'\s*```$', '', raw_text, flags=re.IGNORECASE)
            raw_text = raw_text.strip()

            return json.loads(raw_text)

        except json.JSONDecodeError as json_err:
            print(f"\n[JSON DECODE ERROR] Failed to parse JSON in block {analyzer.__class__.__name__}: {json_err}")
            print(f"[RAW TEXT FROM OLLAMA]:\n{raw_text}\n") # Будем видеть, где именно модель забыла запятую
            return {}
        except Exception as e:
            print(f"\n[CRITICAL OLLAMA ERROR] Failed in block {analyzer.__class__.__name__}:")
            import traceback
            traceback.print_exc()
            return {}

    async def run_full_analysis(self, vacancy: Any, resume: str, cover_letter: str, user_criteria: str) -> Tuple[float, str, List[str]]:
        summary_data = await self.summary_orch.generate_summary(vacancy, resume, cover_letter, user_criteria)
        psychology_data = await self.psychology_orch.generate_portrait(vacancy, resume, cover_letter, user_criteria)

        # Извлекаем оценки безопасности и технического мэтча
        compliance = summary_data.get("compliance_analysis", {})
        tech_score = compliance.get("ai_score", 0.0)

        culture_fit = summary_data.get("culture_fit_analysis", {})
        culture_score = culture_fit.get("culture_fit_score", tech_score)

        final_ai_score = round((tech_score * 0.7) + (culture_score * 0.3), 2)

        combined_analysis = {
            "general_summary": summary_data,
            "psychological_portrait": psychology_data
        }

        extracted_skills = compliance.get("key_competencies", [])
        
        return (
            final_ai_score, 
            json.dumps(combined_analysis, ensure_ascii=False), 
            extracted_skills
        )
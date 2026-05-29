import asyncio
import grpc

# Импортируем динамически скорректированные сгенерированные gRPC модули
import generated.analyzer_pb2 as analyzer_pb2
import generated.analyzer_pb2_grpc as analyzer_pb2_grpc

from services.main_orchestrator import MainAnalysisOrchestrator

class AnalyzerHandler(analyzer_pb2_grpc.AnalyzerServiceServicer):
    """
    gRPC-хендлер, обрабатывающий входящие запросы.
    Наследуется от сгенерированного базового класса Servicer.
    """
    def __init__(self):
        # Инициализируем наш оркестратор (модель по умолчанию - llama3)
        self.orchestrator = MainAnalysisOrchestrator(model_name="llama3")

    def AnalyzeCandidate(self, request: analyzer_pb2.AnalyzeRequest, context: grpc.ServicerContext) -> analyzer_pb2.AnalyzeResponse:
        print(f"[gRPC Handler] Processing structured analysis request...")

        # 1. Валидация наличия вакансии и резюме (Guard Clauses)
        if not request.HasField("vacancy") or not request.vacancy.title.strip():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Vacancy context with a valid title must be provided.")
            return analyzer_pb2.AnalyzeResponse()

        if not request.resume_text.strip():
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Resume text cannot be empty.")
            return analyzer_pb2.AnalyzeResponse()

        try:
            # 2. Перенаправляем асинхронную задачу оркестратору внутри текущего потока
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            ai_score, ai_analysis_json, extracted_skills = loop.run_until_complete(
                self.orchestrator.run_full_analysis(
                    vacancy=request.vacancy,
                    resume=request.resume_text,
                    cover_letter=request.cover_letter,
                    user_criteria=request.user_criteria
                )
            )
            loop.close()

            # 3. Возвращаем строго типизированный ответ
            return analyzer_pb2.AnalyzeResponse(
                ai_score=ai_score,
                ai_analysis_json=ai_analysis_json,
                extracted_skills=extracted_skills
            )

        except Exception as e:
            print(f"[gRPC Handler Error] Critical failure: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal AI error: {str(e)}")
            return analyzer_pb2.AnalyzeResponse()
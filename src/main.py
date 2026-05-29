from concurrent import futures
import sys
import os
import time
import grpc

# Добавляем корневой путь src в sys.path, чтобы Python 
# корректно разрешал импорты модулей из любых директорий
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Подключаем исправление путей для сгенерированных gRPC файлов
import generated
import generated.analyzer_pb2_grpc as analyzer_pb2_grpc
from handlers.analyzer_handler import AnalyzerHandler

def serve():
    # 1. Создаем пул потоков для обработки входящих вызовов (аналог Worker Threads в .NET)
    # 5 потоков вполне достаточно, так как основная нагрузка будет уходить в Ollama
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    
    # 2. Регистрируем наш gRPC хендлер на сервере
    analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(AnalyzerHandler(), server)
    
    # 3. Настраиваем хост и порт (порт :5105, как заложено в архитектуре AiTalentGenome)
    listen_addr = "0.0.0.0:5105"
    server.add_insecure_port(listen_addr)
    
    print(f"[Python gRPC Server] AnalyzerService successfully started on http://{listen_addr}")
    print("Press Ctrl+C to stop.")
    
    server.start()
    
    # 4. Держим главный поток активным, чтобы сервер не завершал работу
    try:
        while True:
            time.sleep(86400)  # Спим сутки
    except KeyboardInterrupt:
        print("\n[Python gRPC Server] Stopping gracefully...")
        # Даем 5 секунд на завершение текущих активных gRPC запросов перед выключением
        server.stop(grace=5)
        print("[Python gRPC Server] Stopped.")

if __name__ == "__main__":
    serve()
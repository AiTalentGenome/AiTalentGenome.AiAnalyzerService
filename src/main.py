from concurrent import futures
import sys
import os
import time
import grpc

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import generated
import generated.analyzer_pb2_grpc as analyzer_pb2_grpc
from handlers.analyzer_handler import AnalyzerHandler

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    
    analyzer_pb2_grpc.add_AnalyzerServiceServicer_to_server(AnalyzerHandler(), server)
    
    listen_addr = "0.0.0.0:5105"
    server.add_insecure_port(listen_addr)
    
    print(f"[Python gRPC Server] AnalyzerService successfully started on http://{listen_addr}")
    print("Press Ctrl+C to stop.")
    
    server.start()
    
    try:
        while True:
            time.sleep(86400)  # Спим сутки
    except KeyboardInterrupt:
        print("\n[Python gRPC Server] Stopping gracefully...")
        server.stop(grace=5)
        print("[Python gRPC Server] Stopped.")

if __name__ == "__main__":
    serve()
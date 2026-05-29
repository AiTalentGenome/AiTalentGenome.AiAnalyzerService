import os
import sys

# Добавляем путь текущей директории в sys.path, 
# чтобы сгенерированные файлы gRPC видели друг друга
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
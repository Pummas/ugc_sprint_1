import sys
from pathlib import Path

""" добавляет директорию с кодом в в пути чтобы могли работать импорты"""
BASE_DIR = Path(__file__).parent.parent
src_path = BASE_DIR / "src"
print("src_path:", src_path)
if src_path not in sys.path:
    sys.path.insert(1, str(src_path))

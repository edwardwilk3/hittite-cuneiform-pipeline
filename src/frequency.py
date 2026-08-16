import sys
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).resolve().parent))
from database import CuneiformDatabase

class SignFrequencyAnalyzer:
    def __init__(self, db_path="data/cuneiform.db"):
        self.db = CuneiformDatabase(db_path)
import sys
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).resolve().parent))
from database import CuneiformDatabase

class SignFrequencyAnalyzer:
    def __init__(self, db_path="data/cuneiform.db"):
        self.db = CuneiformDatabase(db_path)
    def compute_frequencies(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT clean_word FROM tokens")
        token_records = cursor.fetchall()

        print (f"Successfully retrieved {len(token_records)} full tokens from the database.")

        sign_counter = Counter()

        for row in token_records:
             token = row["clean_word"]
             if not token:
                continue #skips empty tokens

            # Split hyphen-separated components (determinatives, clitics, etc.)
        components = token.split('-')
        for sign in components:
            sign = sign.strip()
            if sign:
                sign_counter[sign] += 1

        print(f"Counted {len(sign_counter)} unique sign variants.")
        return sign_counter

if __name__ == "__main__":
    analyzer = SignFrequencyAnalyzer()
    analyzer.compute_frequencies()

    # Further processing of token_records can be done here
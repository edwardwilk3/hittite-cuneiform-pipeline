"""
src/tokenizer.py
Hittite Cuneiform Pipeline - Phase 1 Tokenizer
Handles parsing of Hittite transliteration corpus data, tracking structural markers 
(restorations, determinatives, logograms), counting tokens, and upserting into SQLite.
"""

import re
import sys
from pathlib import Path

# Ensure src/ is in python path or import relative to project structure
sys.path.append(str(Path(__file__).resolve().parent))
from database import CuneiformDatabase

class HittiteTokenizer:
    def __init__(self, db_path="data/cuneiform.db"):
        self.db = CuneiformDatabase(db_path)

    def parse_token(self, raw_token):
        """
        Parses an individual transliterated token for epigraphic and linguistic features:
        - Restorations: [...]
        - Determinatives: {...}
        - Sumerograms / Logograms: uppercase or contains periods
        - Syllable breakdown: separated by hyphens (-)
        """
        # Check for restorations (square brackets)
        is_restoration = bool(re.search(r'\[.*?\]', raw_token))
        
        # Check for determinatives (curly braces)
        is_determinative = bool(re.search(r'\{.*?\}', raw_token))
        
        # Clean markers for base form analysis
        clean_form = re.sub(r'[\{\}\[\]]', '', raw_token)
        
        # Check if it's a logogram/Sumerogram (contains uppercase letters or dots)
        is_logogram = any(c.isupper() for c in clean_form) or '.' in clean_form
        
        # Split into constituent signs/syllables by hyphens
        syllables = clean_form.split('-') if '-' in clean_form else [clean_form]

        return {
            "token_raw": raw_token,
            "token_clean": clean_form,
            "is_restoration": is_restoration,
            "is_determinative": is_determinative,
            "is_logogram": is_logogram,
            "syllable_count": len(syllables),
            "syllables": syllables
        }

    def tokenize_text(self, text, source_id="corpus_sample"):
        """
        Processes multi-line corpus text, tokenizes each line, increments token count,
        and prepares records for database insertion.
        """
        total_tokens = 0
        token_records = []
        
        lines = text.strip().split("\n")
        
        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):  # Skip empty lines or comment lines
                continue
                
            raw_tokens = line.split()
            for position, raw_token in enumerate(raw_tokens, start=1):
                total_tokens += 1
                
                parsed = self.parse_token(raw_token)
                
                token_record = {
                    "source_id": source_id,
                    "line_number": line_num,
                    "position_in_line": position,
                    "token_raw": parsed["token_raw"],
                    "token_clean": parsed["token_clean"],
                    "is_restoration": int(parsed["is_restoration"]),
                    "is_determinative": int(parsed["is_determinative"]),
                    "is_logogram": int(parsed["is_logogram"]),
                    "syllable_count": parsed["syllable_count"]
                }
                token_records.append(token_record)
                
        # Upsert records into database via wrapper
        for record in token_records:
            self.db.upsert_token(record)
        
        return total_tokens, token_records

if __name__ == "__main__":
    # Test corpus sample featuring Hittite, Sumerograms, determinatives, and restorations
    sample_text = """
    # KBo 3.1 translation snippet test
    UM-MA {d}UTU-ši LUGAL.GAL URU ha-at-tu-ša
    [nu-uš-ši-kán] QA-TAM-MA e-eš-du
    ha-at-ti-li ki-i iš-tu-wa-ar
    """
    
    print("Initializing Hittite Tokenizer...")
    tokenizer = HittiteTokenizer()
    
    print("Processing sample text...")
    total_tokens, parsed = tokenizer.tokenize_text(sample_text, source_id="KBo_3.1_sample")
    
    print(f"\n--- Tokenization Results ---")
    print(f"Total Tokens Counted: {total_tokens}")
    print(f"Total Records Upserted: {len(parsed)}")
    
    print("\nSample Parsed Token Inspection:")
    for t in parsed[:6]:
        print(
            f"  Line {t['line_number']}, Pos {t['position_in_line']}: "
            f"'{t['token_raw']}' -> Clean: '{t['token_clean']}' | "
            f"Restoration: {bool(t['is_restoration'])}, "
            f"Determinative: {bool(t['is_determinative'])}, "
            f"Logogram: {bool(t['is_logogram'])}"
        )
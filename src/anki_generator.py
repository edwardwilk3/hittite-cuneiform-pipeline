import csv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from frequency import SignFrequencyAnalyzer

class AnkiDeckGenerator:
    def __init__(self, db_path="data/cuneiform.db"):
        self.analyzer = SignFrequencyAnalyzer(db_path)

    def generate_deck(self, output_path="data/anki_import.txt"):
        counts = self.analyzer.compute_frequencies()
        if not counts:
            print("Error: No sign frequencies found to generate deck.")
            return

        total_occurrences = sum(counts.values())
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Variant labels
        ordinal_labels = ["", "", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth"]

        # Map unicode subscrips to standard ASCII
        subscript_normalizer = str.maketrans("₂₃₄₅₆₇₈₉", "23456789")

        card_count = 0
        with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
            for sign, freq in counts.most_common():
                percentage = (freq / total_occurrences) * 100

                reading = sign
                variant_info = "Primary Sign"

                # Normalize subscript characters
                normalized_sign= sign.translate(subscript_normalizer)

                for char in normalized_sign:
                    if char.isdigit():
                        digit_val = int(char)
                        if 2 <= digit_val < len(ordinal_labels):
                            variant_info = f"{ordinal_labels[digit_val]} Variant"
                            break

                front_field = sign
                back_field = f"{reading}, {variant_info}, [{percentage:.2f}%]"

                outfile.write(f"{front_field}\t{back_field}\n")
                card_count += 1
        print(f"Successfully generated {card_count} Anki flashcard entries at {output_path}")

if __name__ == "__main__":
    generator = AnkiDeckGenerator()
    generator.generate_deck()
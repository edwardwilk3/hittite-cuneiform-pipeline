import re

def tokenize_line(line: str) -> list:
    raw_blocks = line.split()
    token_list = []

    for block in raw_blocks:
        is_gloss = block.startswith(":")
        clean_word = block.lstrip(":")

        is_restored = "[" in clean_word and "]" in clean_word

        stripped_word = clean_word.replace("[", "").replace("]", "")
        
        det_match = re.search(r"(\{([^}]+)\}|<sup>(.*?)</sup>)", stripped_word)
        determinative = None

        if det_match:
            determinative = det_match.group(2) or det_match.group(3)

        if "-" in stripped_word:
            individual_signs = stripped_word.split("-")
        else:
            individual_signs = [stripped_word]

        token_data = {
            "raw_block": block,
            "clean_word": clean_word,
            "is_gloss_wedge": is_gloss,
            "is_restored": is_restored,
            "determinative": determinative,
            "signs": individual_signs
        }

        token_list.append(token_data)

    return token_list
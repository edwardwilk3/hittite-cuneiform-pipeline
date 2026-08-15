from src.cleaner import normalize_brackets
from src.tokenizer import tokenize_line

sample_text = "EGIR-pa :lu-u-wa-i-ti-iš <sup>LÚ</sup>SANGA [zi-la-ti-ya]"

cleaned_text = normalize_brackets(sample_text)

print("Cleaned Text:")
print(cleaned_text)

print("\nTokens:")
tokens = tokenize_line(cleaned_text)

for token in tokens:
    print(token)

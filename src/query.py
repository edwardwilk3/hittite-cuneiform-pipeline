from database import CuneiformDatabase


def run_tests():
  print("Initializing database test...")
  db = CuneiformDatabase("data/cuneiform.db")

  # Sample test tokens mimicking tokenizer output
  test_tokens = [
      {
          "raw_block": "[DINGIR]MEŠ",
          "clean_word": "AN-MEŠ",
          "is_gloss_wedge": False,
          "is_restored": True,
          "determinative": "DINGIR",
          "signs": ["AN", "MEŠ"],
      },
      {
          "raw_block": "UD-az",
          "clean_word": "UD-az",
          "is_gloss_wedge": False,
          "is_restored": False,
          "determinative": None,
          "signs": ["UD", "AZ"],
      },
  ]

  # Insert / Upsert test tokens
  print("Upserting test tokens into SQLite...")
  for token in test_tokens:
    db.upsert_token(token)

  # Query and display records
  print("\nQuerying stored tokens:")
  cursor = db.conn.execute("SELECT * FROM tokens")
  rows = cursor.fetchall()

  for row in rows:
    print(
        f"ID: {row['id']} | Word: {row['clean_word']} | Restored:"
        f" {bool(row['is_restored'])} | Signs: {row['signs']}"
    )

  db.close()
  print("\nDatabase test completed successfully.")


if __name__ == "__main__":
  run_tests()
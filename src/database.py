import os
import sqlite3
from pathlib import Path

class CuneiformDatabase:

    def __init__(self, db_path="data/cuneiform.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.connect()
        self.create_schema()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def create_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    raw_block TEXT,
                    clean_word TEXT,
                    is_gloss_wedge INTEGER,
                    is_restored INTEGER,
                    determinative TEXT,
                    signs TEXT,
                    UNIQUE(raw_block, clean_word, determinative)
                )
            """)
    def upsert_token(self, token_dict):
        with self.conn:
            self.conn.execute(
            """
                INSERT INTO tokens (raw_block, clean_word, is_gloss_wedge, is_restored, determinative, signs)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(raw_block, clean_word, determinative) 
                DO UPDATE SET
                    is_gloss_wedge = excluded.is_gloss_wedge,
                    is_restored = excluded.is_restored,
                    signs = excluded.signs
            """,
             (
                 token_dict.get("raw_block"),
                 token_dict.get("clean_word"),
                 int(token_dict.get("is_gloss_wedge", 0)),
                 int(token_dict.get("is_restored", 0)),
                 token_dict.get("determinative"),
                 ",".join(token_dict.get("signs", [])),
             ),
            )

    def close(self):
            if self.conn:
                self.conn.close()
        
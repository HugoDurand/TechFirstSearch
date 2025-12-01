#!/usr/bin/env python3
"""
Migration script to add AI summary columns to the content table.
Run this script to add the ai_summary and ai_key_points columns.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from database import engine


def add_ai_columns():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE content ADD COLUMN ai_summary TEXT"))
            print("✓ Added ai_summary column")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("⊘ ai_summary column already exists")
            else:
                print(f"✗ Error adding ai_summary: {e}")
        
        try:
            conn.execute(text("ALTER TABLE content ADD COLUMN ai_key_points JSON"))
            print("✓ Added ai_key_points column")
        except Exception as e:
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print("⊘ ai_key_points column already exists")
            else:
                print(f"✗ Error adding ai_key_points: {e}")
        
        conn.commit()
        print("\n✓ Migration completed!")


if __name__ == "__main__":
    print("Adding AI summary columns to database...")
    add_ai_columns()


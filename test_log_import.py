import unittest
import sqlite3
import os
from import_logs import import_from_csv

TEST_DB = "test_logs.db"
TEST_CSV = "test_logs.csv"

class TestLogImport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(TEST_CSV, "w", encoding="utf-8") as f:
            f.write("timestamp,user_id,search_query,response_time\n")
            f.write("2025-04-23 14:32:00,test_user_1,test query 1,0.523\n")
            f.write("2025-04-23 14:33:00,test_user_2,test query 2,0.427\n")

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        import_from_csv(TEST_CSV, TEST_DB)

    def test_table_created(self):
        conn = sqlite3.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='search_logs'")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()

    def test_entries_inserted(self):
        conn = sqlite3.connect(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM search_logs")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)
        conn.close()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_CSV):
            os.remove(TEST_CSV)
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

if __name__ == '__main__':
    unittest.main()

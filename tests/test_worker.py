import unittest
from worker import insert_to_db

class TestWorker(unittest.TestCase):

    def test_insert_to_db(self):
        # Example test for database insertion
        row = ('value1', 'value2', 'value3')
        try:
            insert_to_db(row)
        except Exception as e:
            self.fail(f"insert_to_db raised an exception: {e}")
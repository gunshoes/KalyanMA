import os
import tempfile
import unittest

from src.db.backend.errors import ValidationError
from src.db.backend.file import CsvBookTable
from src.db.backend.file import JsonBookTable


class TestJsonBookTable(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "books.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_json_save_and_load(self):
        table = JsonBookTable(self.file_path)
        table.add("Книга 1", "Автор 1", 2001)
        table.add("Книга 2", "Автор 2", 2002)

        new_table = JsonBookTable(self.file_path)
        books = new_table.get_all()

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "Книга 1")
        self.assertEqual(books[1]["title"], "Книга 2")

    def test_json_update_saved(self):
        table = JsonBookTable(self.file_path)
        table.add("Книга", "Автор", 2000)
        table.update(1, title="Новая книга")

        new_table = JsonBookTable(self.file_path)
        books = new_table.get_all()

        self.assertEqual(books[0]["title"], "Новая книга")

    def test_json_delete_saved(self):
        table = JsonBookTable(self.file_path)
        table.add("Книга", "Автор", 2000)
        table.delete(1)

        new_table = JsonBookTable(self.file_path)
        books = new_table.get_all()

        self.assertEqual(len(books), 0)

    def test_json_next_id_after_load(self):
        table = JsonBookTable(self.file_path)
        table.add("Книга 1", "Автор 1", 2001)

        new_table = JsonBookTable(self.file_path)
        book = new_table.add("Книга 2", "Автор 2", 2002)

        self.assertEqual(book["id"], 2)

    def test_bad_json_file_error(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("bad json")

        with self.assertRaises(ValidationError):
            JsonBookTable(self.file_path)


class TestCsvBookTable(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "books.csv")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_csv_save_and_load(self):
        table = CsvBookTable(self.file_path)
        table.add("Книга 1", "Автор 1", 2001)
        table.add("Книга 2", "Автор 2", 2002)

        new_table = CsvBookTable(self.file_path)
        books = new_table.get_all()

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "Книга 1")
        self.assertEqual(books[1]["title"], "Книга 2")

    def test_csv_update_saved(self):
        table = CsvBookTable(self.file_path)
        table.add("Книга", "Автор", 2000)
        table.update(1, title="Новая книга")

        new_table = CsvBookTable(self.file_path)
        books = new_table.get_all()

        self.assertEqual(books[0]["title"], "Новая книга")

    def test_csv_delete_saved(self):
        table = CsvBookTable(self.file_path)
        table.add("Книга", "Автор", 2000)
        table.delete(1)

        new_table = CsvBookTable(self.file_path)
        books = new_table.get_all()

        self.assertEqual(len(books), 0)

    def test_csv_next_id_after_load(self):
        table = CsvBookTable(self.file_path)
        table.add("Книга 1", "Автор 1", 2001)

        new_table = CsvBookTable(self.file_path)
        book = new_table.add("Книга 2", "Автор 2", 2002)

        self.assertEqual(book["id"], 2)

    def test_bad_csv_file_error(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("bad,data\n1,2\n")

        with self.assertRaises(ValidationError):
            CsvBookTable(self.file_path)


if __name__ == "__main__":
    unittest.main()
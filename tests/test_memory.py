import unittest

from src.db.backend.errors import RecordNotFoundError
from src.db.backend.errors import ValidationError
from src.db.backend.memory import BookTable


class TestBookTable(unittest.TestCase):
    def setUp(self):
        self.table = BookTable()

    def test_add_book(self):
        book = self.table.add("Преступление и наказание", "Достоевский", 1866)

        self.assertEqual(book["id"], 1)
        self.assertEqual(book["title"], "Преступление и наказание")
        self.assertEqual(book["author"], "Достоевский")
        self.assertEqual(book["year"], 1866)

    def test_get_all_books(self):
        self.table.add("Книга 1", "Автор 1", 2001)
        self.table.add("Книга 2", "Автор 2", 2002)

        books = self.table.get_all()

        self.assertEqual(len(books), 2)

    def test_filter_by_title(self):
        self.table.add("Мастер и Маргарита", "Булгаков", 1967)
        self.table.add("Идиот", "Достоевский", 1869)

        books = self.table.filter(title="мастер")

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Мастер и Маргарита")

    def test_filter_by_author(self):
        self.table.add("Мастер и Маргарита", "Булгаков", 1967)
        self.table.add("Идиот", "Достоевский", 1869)

        books = self.table.filter(author="достоевский")

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["author"], "Достоевский")

    def test_filter_by_year(self):
        self.table.add("Книга 1", "Автор 1", 2001)
        self.table.add("Книга 2", "Автор 2", 2002)

        books = self.table.filter(year=2002)

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["year"], 2002)

    def test_update_book(self):
        self.table.add("Старое название", "Старый автор", 2000)

        book = self.table.update(1, title="Новое название", author="Новый автор", year=2020)

        self.assertEqual(book["title"], "Новое название")
        self.assertEqual(book["author"], "Новый автор")
        self.assertEqual(book["year"], 2020)

    def test_update_only_title(self):
        self.table.add("Старое название", "Автор", 2000)

        book = self.table.update(1, title="Новое название")

        self.assertEqual(book["title"], "Новое название")
        self.assertEqual(book["author"], "Автор")
        self.assertEqual(book["year"], 2000)

    def test_delete_book(self):
        self.table.add("Книга", "Автор", 2000)

        book = self.table.delete(1)
        books = self.table.get_all()

        self.assertEqual(book["id"], 1)
        self.assertEqual(len(books), 0)

    def test_sort_by_year_asc(self):
        self.table.add("Книга 1", "Автор 1", 2003)
        self.table.add("Книга 2", "Автор 2", 2001)
        self.table.add("Книга 3", "Автор 3", 2002)

        books = self.table.sort("year")

        self.assertEqual(books[0]["year"], 2001)
        self.assertEqual(books[1]["year"], 2002)
        self.assertEqual(books[2]["year"], 2003)

    def test_sort_by_year_desc(self):
        self.table.add("Книга 1", "Автор 1", 2003)
        self.table.add("Книга 2", "Автор 2", 2001)
        self.table.add("Книга 3", "Автор 3", 2002)

        books = self.table.sort("year", reverse=True)

        self.assertEqual(books[0]["year"], 2003)
        self.assertEqual(books[1]["year"], 2002)
        self.assertEqual(books[2]["year"], 2001)

    def test_empty_title_error(self):
        with self.assertRaises(ValidationError):
            self.table.add("", "Автор", 2000)

    def test_empty_author_error(self):
        with self.assertRaises(ValidationError):
            self.table.add("Книга", "", 2000)

    def test_bad_year_error(self):
        with self.assertRaises(ValidationError):
            self.table.add("Книга", "Автор", "abc")

    def test_negative_year_error(self):
        with self.assertRaises(ValidationError):
            self.table.add("Книга", "Автор", -1)

    def test_bad_id_error(self):
        with self.assertRaises(ValidationError):
            self.table.update("abc", title="Название")

    def test_record_not_found_error(self):
        with self.assertRaises(RecordNotFoundError):
            self.table.delete(100)

    def test_bad_sort_field_error(self):
        self.table.add("Книга", "Автор", 2000)

        with self.assertRaises(ValidationError):
            self.table.sort("bad_field")


if __name__ == "__main__":
    unittest.main()
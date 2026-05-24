from src.db.backend.errors import RecordNotFoundError
from src.db.backend.errors import ValidationError


class BookRecord:
    def __init__(self, record_id, title, author, year):
        self.id = record_id
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }


class BookTable:
    def __init__(self):
        self.records = []
        self.next_id = 1

    def add(self, title, author, year):
        title = self._validate_text(title, "Название книги")
        author = self._validate_text(author, "Автор")
        year = self._validate_year(year)

        record = BookRecord(self.next_id, title, author, year)
        self.records.append(record)
        self.next_id += 1

        return record.to_dict()

    def get_all(self):
        result = []

        for record in self.records:
            result.append(record.to_dict())

        return result

    def filter(self, title=None, author=None, year=None):
        if year is not None and year != "":
            year = self._validate_year(year)

        result = []

        for record in self.records:
            good = True

            if title is not None and title != "":
                if title.lower() not in record.title.lower():
                    good = False

            if author is not None and author != "":
                if author.lower() not in record.author.lower():
                    good = False

            if year is not None and year != "":
                if record.year != year:
                    good = False

            if good:
                result.append(record.to_dict())

        return result

    def update(self, record_id, title=None, author=None, year=None):
        record_id = self._validate_id(record_id)
        record = self._find_record(record_id)

        if title is not None and title != "":
            record.title = self._validate_text(title, "Название книги")

        if author is not None and author != "":
            record.author = self._validate_text(author, "Автор")

        if year is not None and year != "":
            record.year = self._validate_year(year)

        return record.to_dict()

    def delete(self, record_id):
        record_id = self._validate_id(record_id)
        record = self._find_record(record_id)

        self.records.remove(record)

        return record.to_dict()
    def _get_next_id(self):
        max_id = 0

        for record in self.records:
            if record.id > max_id:
                max_id = record.id

        return max_id + 1

    def sort(self, field, reverse=False):
        allowed_fields = ["id", "title", "author", "year"]

        if field not in allowed_fields:
            raise ValidationError("Нельзя сортировать по такому полю")

        sorted_records = sorted(
            self.records,
            key=lambda record: getattr(record, field),
            reverse=reverse,
        )

        result = []

        for record in sorted_records:
            result.append(record.to_dict())

        return result

    def _find_record(self, record_id):
        for record in self.records:
            if record.id == record_id:
                return record

        raise RecordNotFoundError("Книга с таким ID не найдена")

    def _validate_id(self, record_id):
        try:
            record_id = int(record_id)
        except ValueError:
            raise ValidationError("ID должен быть числом")

        if record_id <= 0:
            raise ValidationError("ID должен быть положительным числом")

        return record_id

    def _validate_text(self, value, field_name):
        if value is None:
            raise ValidationError(f"{field_name} не может быть пустым")

        value = value.strip()

        if value == "":
            raise ValidationError(f"{field_name} не может быть пустым")

        return value

    def _validate_year(self, year):
        try:
            year = int(year)
        except ValueError:
            raise ValidationError("Год должен быть числом")

        if year <= 0:
            raise ValidationError("Год должен быть положительным числом")

        return year


book_table = BookTable()


def add_book(title, author, year):
    return book_table.add(title, author, year)


def get_books(title=None, author=None, year=None):
    if title is None and author is None and year is None:
        return book_table.get_all()

    return book_table.filter(title, author, year)


def update_book(book_id, title=None, author=None, year=None):
    return book_table.update(book_id, title, author, year)


def delete_book(book_id):
    return book_table.delete(book_id)


def sort_books(field, reverse=False):
    return book_table.sort(field, reverse)
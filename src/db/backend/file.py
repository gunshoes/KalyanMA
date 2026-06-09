import csv
import json
import os

from src.db.backend.errors import ValidationError
from src.db.backend.memory import BookRecord
from src.db.backend.memory import BookTable


class JsonBookTable(BookTable):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.columns = ["id", "title", "author", "year"]
        self.load()

    def add(self, title, author, year):
        book = super().add(title, author, year)
        self.save()
        return book

    def update(self, record_id, title=None, author=None, year=None):
        book = super().update(record_id, title, author, year)
        self.save()
        return book

    def delete(self, record_id):
        book = super().delete(record_id)
        self.save()
        return book

    def save(self):
        folder = os.path.dirname(self.file_path)

        if folder != "":
            os.makedirs(folder, exist_ok=True)

        data = {
            "columns": self.columns,
            "records": self.get_all(),
            "next_id": self.next_id,
        }

        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            raise ValidationError("Ошибка записи JSON файла")

    def load(self):
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except OSError:
            raise ValidationError("Ошибка чтения JSON файла")
        except json.JSONDecodeError:
            raise ValidationError("Некорректный JSON файл")

        self._load_from_data(data)

    def _load_from_data(self, data):
        if "columns" not in data or "records" not in data:
            raise ValidationError("Некорректная структура JSON файла")

        if data["columns"] != self.columns:
            raise ValidationError("Некорректная структура JSON файла")

        if not isinstance(data["records"], list):
            raise ValidationError("Некорректная структура JSON файла")

        self.records = []

        for item in data["records"]:
            try:
                record = BookRecord(
                    item["id"],
                    item["title"],
                    item["author"],
                    item["year"],
                )
            except KeyError:
                raise ValidationError("Некорректная структура записи JSON файла")

            self.records.append(record)

        if "next_id" in data:
            if not isinstance(data["next_id"], int) or data["next_id"] < 1:
                raise ValidationError("Некорректное значение next_id в JSON файле")

            self.next_id = data["next_id"]
        else:
            self.next_id = self._get_next_id()


class CsvBookTable(BookTable):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.columns = ["id", "title", "author", "year"]
        self.load()

    def add(self, title, author, year):
        book = super().add(title, author, year)
        self.save()
        return book

    def update(self, record_id, title=None, author=None, year=None):
        book = super().update(record_id, title, author, year)
        self.save()
        return book

    def delete(self, record_id):
        book = super().delete(record_id)
        self.save()
        return book

    def save(self):
        folder = os.path.dirname(self.file_path)

        if folder != "":
            os.makedirs(folder, exist_ok=True)

        try:
            with open(self.file_path, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.columns)
                writer.writeheader()

                for record in self.get_all():
                    writer.writerow(record)
        except OSError:
            raise ValidationError("Ошибка записи CSV файла")

    def load(self):
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames != self.columns:
                    raise ValidationError("Некорректная структура CSV файла")

                self.records = []

                for item in reader:
                    record = BookRecord(
                        int(item["id"]),
                        item["title"],
                        item["author"],
                        int(item["year"]),
                    )
                    self.records.append(record)

                self.next_id = self._get_next_id()
        except OSError:
            raise ValidationError("Ошибка чтения CSV файла")
        except ValueError:
            raise ValidationError("Некорректные данные в CSV файле")

    def _get_next_id(self):
        max_id = 0

        for record in self.records:
            if record.id > max_id:
                max_id = record.id

        return max_id + 1

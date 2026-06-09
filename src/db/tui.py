from src.db.backend.errors import DatabaseError
from src.db.backend.file import CsvBookTable, JsonBookTable
from src.db.backend.memory import BookTable


class ConsoleInterface:
    def __init__(self):
        self.table = self.choose_storage()

    def choose_storage(self):
        print("Выберите тип хранилища:")
        print("1. In-memory")
        print("2. JSON")
        print("3. CSV")

        choice = input("Ваш выбор: ")

        if choice == "1":
            return BookTable()
        if choice == "2":
            return JsonBookTable("books.json")
        if choice == "3":
            return CsvBookTable("books.csv")

        print("Неизвестный тип хранилища, используется In-memory")
        return BookTable()

    def show_menu(self):
        print()
        print("База данных книг")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("6. Сортировать книги")
        print("0. Выход")

    def print_books(self, books):
        if len(books) == 0:
            print("Записей нет")
            return

        for book in books:
            print(
                f"ID: {book['id']}, "
                f"Название: {book['title']}, "
                f"Автор: {book['author']}, "
                f"Год: {book['year']}"
            )

    def add_book_menu(self):
        title = input("Введите название книги: ")
        author = input("Введите автора: ")
        year = input("Введите год: ")

        book = self.table.add(title, author, year)
        print("Книга добавлена:")
        self.print_books([book])

    def show_all_books_menu(self):
        books = self.table.get_all()
        self.print_books(books)

    def search_books_menu(self):
        print("Оставьте поле пустым, если не хотите фильтровать по нему")

        title = input("Название: ")
        author = input("Автор: ")
        year = input("Год: ")

        books = self.table.filter(title, author, year)
        self.print_books(books)

    def update_book_menu(self):
        book_id = input("Введите ID книги: ")

        print("Оставьте поле пустым, если не хотите менять его")
        title = input("Новое название: ")
        author = input("Новый автор: ")
        year = input("Новый год: ")

        book = self.table.update(book_id, title, author, year)
        print("Книга обновлена:")
        self.print_books([book])

    def delete_book_menu(self):
        book_id = input("Введите ID книги: ")

        book = self.table.delete(book_id)
        print("Книга удалена:")
        self.print_books([book])

    def sort_books_menu(self):
        print("Поля для сортировки: id, title, author, year")

        field = input("Введите поле для сортировки: ")
        direction = input("Порядок сортировки asc/desc: ")

        reverse = False

        if direction == "desc":
            reverse = True
        elif direction != "asc":
            print("Неизвестный порядок сортировки, используется asc")

        books = self.table.sort(field, reverse)
        self.print_books(books)

    def start(self):
        while True:
            self.show_menu()
            command = input("Выберите действие: ")

            try:
                if command == "1":
                    self.add_book_menu()
                elif command == "2":
                    self.show_all_books_menu()
                elif command == "3":
                    self.search_books_menu()
                elif command == "4":
                    self.update_book_menu()
                elif command == "5":
                    self.delete_book_menu()
                elif command == "6":
                    self.sort_books_menu()
                elif command == "0":
                    print("Выход")
                    break
                else:
                    print("Такой команды нет")
            except DatabaseError as error:
                print("Ошибка:", error)


def start():
    interface = ConsoleInterface()
    interface.start()


if __name__ == "__main__":
    start()
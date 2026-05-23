from src.db.backend.memory import add_book
from src.db.backend.memory import delete_book
from src.db.backend.memory import get_books
from src.db.backend.memory import update_book


def show_menu():
    print()
    print("In-memory база данных книг")
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Найти книги")
    print("4. Обновить книгу")
    print("5. Удалить книгу")
    print("0. Выход")


def print_books(books):
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


def add_book_menu():
    title = input("Введите название книги: ")
    author = input("Введите автора: ")
    year = input("Введите год: ")

    book = add_book(title, author, year)
    print("Книга добавлена:")
    print_books([book])


def show_all_books_menu():
    books = get_books()
    print_books(books)


def search_books_menu():
    print("Оставьте поле пустым, если не хотите фильтровать по нему")

    title = input("Название: ")
    author = input("Автор: ")
    year = input("Год: ")

    if title == "":
        title = None

    if author == "":
        author = None

    if year == "":
        year = None

    books = get_books(title, author, year)
    print_books(books)


def update_book_menu():
    book_id = input("Введите ID книги: ")

    print("Оставьте поле пустым, если не хотите менять его")
    title = input("Новое название: ")
    author = input("Новый автор: ")
    year = input("Новый год: ")

    book = update_book(book_id, title, author, year)
    print("Книга обновлена:")
    print_books([book])


def delete_book_menu():
    book_id = input("Введите ID книги: ")

    book = delete_book(book_id)
    print("Книга удалена:")
    print_books([book])


def start():
    while True:
        show_menu()
        command = input("Выберите действие: ")

        try:
            if command == "1":
                add_book_menu()
            elif command == "2":
                show_all_books_menu()
            elif command == "3":
                search_books_menu()
            elif command == "4":
                update_book_menu()
            elif command == "5":
                delete_book_menu()
            elif command == "0":
                print("Выход")
                break
            else:
                print("Такой команды нет")
        except ValueError as error:
            print("Ошибка:", error)
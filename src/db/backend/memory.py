books = []
next_id = 1


def add_book(title, author, year):
    global next_id

    if title == "":
        raise ValueError("Название книги не может быть пустым")

    if author == "":
        raise ValueError("Автор не может быть пустым")

    try:
        year = int(year)
    except ValueError:
        raise ValueError("Год должен быть числом")

    if year <= 0:
        raise ValueError("Год должен быть положительным числом")

    book = {
        "id": next_id,
        "title": title,
        "author": author,
        "year": year,
    }

    books.append(book)
    next_id += 1

    return book


def get_books(title=None, author=None, year=None):
    result = []

    for book in books:
        good = True

        if title is not None and title.lower() not in book["title"].lower():
            good = False

        if author is not None and author.lower() not in book["author"].lower():
            good = False

        if year is not None:
            try:
                year = int(year)
            except ValueError:
                raise ValueError("Год должен быть числом")

            if book["year"] != year:
                good = False

        if good:
            result.append(book)

    return result


def update_book(book_id, title=None, author=None, year=None):
    try:
        book_id = int(book_id)
    except ValueError:
        raise ValueError("ID должен быть числом")

    for book in books:
        if book["id"] == book_id:
            if title is not None and title != "":
                book["title"] = title

            if author is not None and author != "":
                book["author"] = author

            if year is not None and year != "":
                try:
                    year = int(year)
                except ValueError:
                    raise ValueError("Год должен быть числом")

                if year <= 0:
                    raise ValueError("Год должен быть положительным числом")

                book["year"] = year

            return book

    raise ValueError("Книга с таким ID не найдена")


def delete_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        raise ValueError("ID должен быть числом")

    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return book

    raise ValueError("Книга с таким ID не найдена")
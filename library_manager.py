import json
import os


class Book:
    def __init__(self, title, author, year):
        self.id = None  # Идентификатор будет назначен позже
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }


class Library:
    def __init__(self, filename='books.json'):
        self.filename = filename
        self.books = []
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                for book in books_data:
                    book_obj = Book(book['title'], book['author'], book['year'])
                    book_obj.id = book['id']
                    book_obj.status = book['status']
                    self.books.append(book_obj)
                return self.books
        return []

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        new_book = Book(title, author, year)
        new_book.id = len(self.books) + 1  # Генерация уникального id
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, id):
        for book in self.books:
            if book.id == id:
                self.books.remove(book)
                self.save_books()
                return f'Книга с ID {id} удалена.'
        return 'Книга не найдена.'

    def search_books(self, query):
        results = [
            book for book in self.books
            if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in str(
                book.year)
        ]
        return results

    def display_books(self):
        return [book.to_dict() for book in self.books]

    def update_status(self, id, status):
        for book in self.books:
            if book.id == id:
                if status in ["в наличии", "выдана"]:
                    book.status = status
                    self.save_books()
                    return f'Статус книги с ID {id} изменён на {status}.'
                else:
                    return 'Статус должен быть "в наличии" или "выдана".'
        return 'Книга не найдена.'


def main():
    library = Library()
    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)
            print("Книга добавлена.")

        elif choice == '2':
            id = int(input("Введите ID книги для удаления: "))
            print(library.remove_book(id))

        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = library.search_books(query)
            if results:
                for book in results:
                    print(book.to_dict())
            else:
                print("Книги не найдены.")

        elif choice == '4':
            books = library.display_books()
            if books:
                for book in books:
                    print(book)
            else:
                print("Библиотека пуста.")

        elif choice == '5':
            id = int(input("Введите ID книги для изменения статуса: "))
            status = input("Введите новый статус (в наличии/выдана): ")
            print(library.update_status(id, status))

        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == '__main__':
    main()
from conf import MODEL
import random
from faker import Faker
import json
fake = Faker("ru")

def title_book() -> str:
    """
    :return: Возращает случайное название книги из файла
    """
    with open('books.txt', encoding="UTF-8") as f:
        title = random.choice(f.readlines())
    return title.rstrip()


def year_book() -> int:
    """
    :return: Генерирует случайный год
    """
    year_book = int(fake.year())
    return year_book


def pages_book(min: int=1, max: int=1000) -> int:
    """
    Генерирует случайное количество страниц. Диапазон по умолчанию от 50 до 1000 стр.
    :param min: по умолчанию начальное значение диапазона стр. 50
    :param max: по умолчанию конечное значение диапазона стр. 1000
    :return:
    """
    pages_book = random.randint(min, max)
    return pages_book


def isbn13_book() -> str:
    """
    :return: Генерирует случайный isbn (книжный номер)
    """
    isbn_book = fake.isbn13()
    return isbn_book


def rating_book() -> float:
    """
    :return: Возвращает случайное значение рейтинга от 0 до 5
    """
    rating_book = random.uniform(0, 5)
    return round(rating_book, 1)


def price_book(min: float=250, max: float=100000) -> float:
    """
    Возвращает случайное значение стоимости книги
    :param min: минимальная стоимость по умолчанию 250
    :param max: максимальная стоимость по умолчанию 100000
    :return:
    """
    price_book = random.uniform(min, max)
    return round(price_book, 2)


def author_book() -> list:
    """
    :return: Генерирует случайный список авторов от 1 до 3
    """
    author = [f"{fake.first_name()} {fake.last_name()}" for _ in range(random.randint(1, 3))]
    return author


def main(pk: int=1, n: int=100) -> json:
    """
    :param pk: счётчик, который увеличивается на единицу при генерации нового объекта. По умолчанию = 1
    :param n: количество книг (список словарей) по умолчанию 100
    :return: Формирует список из 100 книг (список словарей) и записывает его в json файл
    """
    with open("book.json", "w", encoding="UTF-8") as f:
        for _ in range(n):
            k = ["title", "year", "pages", "isbn13", "rating", "price", "author"]
            v = [title_book(), year_book(), pages_book(), isbn13_book(), rating_book(), price_book(), author_book()]
            book = {"model": MODEL, "pk": pk, "fields": {k: v for (k, v) in zip(k, v)}}
            json.dump(book, f, indent=4)
            pk += 1


if __name__ == '__main__':
    main()
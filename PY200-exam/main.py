import random
import hashlib
import re


class IdCounter:
    """ Генератор значений id """
    def __init__(self, id_data: list = None):
        """
        Инициализируются следующие атрибуты генератора значений id
        :param id_data: Список id
        """
        if id_data is None:
            self.id_data = []
        else:
            self.id_data = id_data

    def current_id(self, id_: int) -> int:
        """ Проверяет текущий id """
        if isinstance(id_, int):
            if id_ in self.id_data:
                return id_
            raise ValueError(f"Введенного id не существует")
        raise TypeError(f"Id должен быть типа 'int'")

    def get_new_id(self) -> int:
        """ Возвращает новый id """
        if not self.id_data:
            self.id_data.append(1)
            return 1
        id_ = self.id_data.__getitem__(-1) + 1
        self.id_data.append(id_)
        return id_


class Password:
    """ Класс ответственен за выдачу хэш-значения пароля """
    @classmethod
    def get_hash(cls, password: str) -> str:
        """ Выдает хэш-значения пароля """
        if cls.is_valid(password):
            return hashlib.sha256(password.encode()).hexdigest()
        return "Необходимо выбрать другой пароль"

    @staticmethod
    def is_valid(password: str) -> bool:
        """ Осуществляет проверку пароля установленным требованиям защищенности """
        pattern = r"^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-zА-Яа-я\d@$!%*#?&]{8,}$"
        if not isinstance(password, str):
            raise TypeError("Пароль должен быть типа 'str'.")
        if re.match(pattern, password) is None:
            raise ValueError("Пароль должен состоять из не менее чем 8 символов, "
                             "содержать цифры, буквы (не менее одной в верхнем регистре), спецсимволы.")
        return True

    @classmethod
    def check(cls, password: str, hash_password: str) -> str:
        if cls.get_hash(password) == hash_password:
            return f"Пароль правильный."
        return f"Пароль введен не правильно."


class Product:
    """ Класс в котором хранится информация о товаре """
    _counter = IdCounter()

    data_base = ['кондиционер', 'посудомоечная машина', 'сушилка для белья',
                 'сушильный шкаф', 'морозильная камера', 'винный шкаф', 'холодильник',
                 'кухонная плита', 'водонагреватель', 'стиральная машина', 'телевизор',
                 'микроволновая печь', 'индукционная плита']

    def __init__(self, name: str, price: float, rating: float):
        """
        Инициализируются атрибуты товара
        :param name: Наименование товара
        :param price: Цена товара в руб.
        :param rating: Рейтинг товара в магазине
        """
        self._id = self._counter.get_new_id()
        self.__name = name
        self.price = price
        self.rating = rating

    def _name_get(self):
        """ Выводит наименование товара. """
        return self.__name

    def _name_set(self, name: str):
        """ Устанавливает наименование товара. """
        self.__name = name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """ Устанавливает цену товара. """
        if value is not None:
            if not isinstance(value, float):
                raise TypeError("Цена товара должна быть типа <float>.")
            if value <= 0:
                raise ValueError("Цена товара должна быть положительном числом больше 0.")
        self._price = value

    @property
    def rating(self) -> float:
        return self._rating

    @rating.setter
    def rating(self, value: float) -> None:
        """ Устанавливает рейтинг товара. """
        if value is not None:
            if not isinstance(value, float):
                raise TypeError("Рейтинг товара должен быть типа <float>.")
            if not 0 <= value <= 10:
                raise ValueError("Рейтинг товара должен быть положительном числом от 0 до 10.")

        self._rating = value

    def get_product(self):
        """ Генератор случайной бытовой техники товара """
        name = random.choice(self.data_base)
        price = round(random.uniform(23000, 117000), 2)
        rating = round(random.uniform(0, 10), 2)
        return name, price, rating

    def __str__(self):
        return f"{self._id}_{self.__name}"

    def __repr__(self):
        return f"(id={self._id}, name={self.__name}, price={self.price}, rating={self.rating})"


class Cart:
    """ Класс 'Корзина', в котором хранится информация о списке товаров"""
    def __init__(self):
        self._data = []

    def add(self, product):
        """ Добавление товара в корзину """
        self._data.append(product)

    def remove(self, product):
        """ Удаление товара из корзины """
        self._data.remove(product)

    def get_data(self):
        """ Выводит список товаров, находящихся в корзине """
        return self._data


class User:
    """ Класс, в котором хранится информация о пользователе """
    _counter = IdCounter()

    def __init__(self, username: str, password: str):
        """
        Инициализируются атрибуты пользователя
        :param username: Имя пользователя
        :param password: Пароль пользователя
        """
        self._id = self._counter.get_new_id()
        self.username = self.check_username(username)
        self.__password = Password.get_hash(password)
        self._cart = Cart()

    def check_username(self, username: str):
        """ Проверяет имя пользователя """
        if username is None:
            if not isinstance(username, str):
                raise TypeError("Имя пользователя должно быть типа <str>.")
            if not username.isalnum():
                raise ValueError("Имя пользователя должно содержать только буквы или цифры.")
            if not username.islower():
                raise ValueError("Имя пользователя должно содержать и буквы, но только нижнего регистра.")
        self._username = username

    def get_username(self):
        return self._username

    def get_cart(self):
        return self._cart

    def __str__(self):
        return f"Пользователь - '{self._username}', пароль - 'password1'"

    def __repr__(self):
        return f"(id={self._id}, username={self._username}, password='password1')"


class Store:
    """ Класс магазин бытовой техники """

    def __init__(self, product_generator):
        self.user = None
        self.authentification()
        self.product_generator = product_generator

    def set_product(self, product_generator):
        self.product_generator = product_generator

    def get_product(self):
        return self.product_generator

    def authentification(self):
        """ Аутентификацию пользователя"""
        if True:
            login = input()
            password = input()
            try:
                self.user = User(login, password)
            except ValueError:
                print("Введена некорреткная пара логин-пароль")

    def add_to_cart(self):
        """ Добавляет случайный товар в корзину """
        product = self.product_generator.get_product()
        self.user._cart.add(product)

    def view_cart(self):
        """ Позволяет пользователю просмотреть свою корзину """
        print(self.user._cart.get_data())

    def __str__(self):
        return f"{self.user}; продукт: {self.product_generator}"


if __name__ == "__main__":
    p = Product('телевизор', 250.20, 2.2)
    s = Store(p)
    print(s)

    s.add_to_cart()
    s.add_to_cart()
    s.add_to_cart()
    s.add_to_cart()
    s.view_cart()

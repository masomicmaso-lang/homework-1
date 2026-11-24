from abc import ABC, abstractmethod


# Шаг 1. Абстрактный класс Storage
class Storage(ABC):
    """
    Абстрактный класс для описания хранилища товаров.
    """

    def __init__(self, items: dict, capacity: int):
        # Инкапсуляция: защищенные атрибуты
        self._items = dict(items)
        self._capacity = capacity

    @abstractmethod
    def add(self, name: str, amount: int) -> bool:
        """Увеличивает количество товара name на amount."""
        pass

    @abstractmethod
    def remove(self, name: str, amount: int) -> bool:
        """Уменьшает количество товара name на amount."""
        pass

    def get_free_space(self) -> int:
        """Возвращает количество свободного места в хранилище."""
        used_space = sum(self._items.values())
        return self._capacity - used_space

    def get_items(self) -> dict:
        """Возвращает текущее содержимое хранилища (копию)."""
        return self._items.copy()

    def get_unique_items_count(self) -> int:
        """Возвращает количество уникальных позиций товара."""
        return len(self._items)


# Шаг 2. Класс Store (Склад)
class Store(Storage):
    """
    Склад. Не имеет ограничений на количество видов товаров.
    """

    def __init__(self, items: dict, capacity: int = 100):
        super().__init__(items, capacity)

    def add(self, name: str, amount: int) -> bool:
        if amount <= 0:
            return False
        if self.get_free_space() < amount:
            return False
        self._items[name] = self._items.get(name, 0) + amount
        return True

    def remove(self, name: str, amount: int) -> bool:
        if name not in self._items or self._items[name] < amount:
            return False
        self._items[name] -= amount
        if self._items[name] == 0:
            del self._items[name]
        return True


# Шаг 3. Класс Shop (Магазин)
class Shop(Storage):
    """
    Магазин. Ограничение: не более 5 уникальных товаров.
    """

    def __init__(self, items: dict, capacity: int = 20):
        super().__init__(items, capacity)

    def add(self, name: str, amount: int) -> bool:
        if amount <= 0:
            return False
        if self.get_free_space() < amount:
            return False
        # Проверка на лимит уникальных товаров (максимум 5)
        if name not in self._items and self.get_unique_items_count() >= 5:
            return False

        self._items[name] = self._items.get(name, 0) + amount
        return True

    def remove(self, name: str, amount: int) -> bool:
        if name not in self._items or self._items[name] < amount:
            return False
        self._items[name] -= amount
        if self._items[name] == 0:
            del self._items[name]
        return True


# Шаг 4. Класс Request (Запрос на перемещение)
class Request:
    """
    Класс для представления и парсинга запроса на перемещение товаров.
    """

    def __init__(self, request_str: str):
        # Разбиваем строку по пробелам
        parts = request_str.strip().lower().split()

        if len(parts) != 7:
            raise ValueError("Неверный формат запроса. Ожидается: 'Доставить <кол-во> <товар> из <откуда> в <куда>'")

        try:
            self.amount = int(parts[1])
            if self.amount <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Количество должно быть целым положительным числом.")

        self.product = parts[2]

        # Извлекаем названия точек (игнорируем предлоги, чтобы работало и "из склада", и "со склада")
        from_point = parts[4]
        to_point = parts[6]

        if from_point.startswith("склад"):
            self.from_point = "склад"
        elif from_point.startswith("магазин"):
            self.from_point = "магазин"
        else:
            raise ValueError("Неизвестное место отправления. Используйте 'склад' или 'магазин'.")

        if to_point.startswith("склад"):
            self.to_point = "склад"
        elif to_point.startswith("магазин"):
            self.to_point = "магазин"
        else:
            raise ValueError("Неизвестное место назначения. Используйте 'склад' или 'магазин'.")

        if self.from_point == self.to_point:
            raise ValueError("Пункты отправления и назначения не могут совпадать.")

    def __str__(self) -> str:
        return f"Доставить {self.amount} {self.product} из {self.from_point} в {self.to_point}"


# Шаг 5. Основная логика программы (main)
def print_storage(name: str, storage: Storage) -> None:
    """Вспомогательная функция для вывода состояния хранилища."""
    print(f"В {name} хранится:")
    items = storage.get_items()
    if not items:
        print("  (пусто)")
    for item, qty in items.items():
        print(f"  {qty} {item}")
    print()


def main():
    # Начальные запасы товаров
    initial_store_items = {"печеньки": 10, "собачки": 10, "коробки": 10, "конфеты": 10, "игрушки": 10}
    initial_shop_items = {"собачки": 2, "коробки": 5}

    # Инициализация хранилищ
    store = Store(items=initial_store_items, capacity=100)
    shop = Shop(items=initial_shop_items, capacity=20)

    # Словарь для быстрого доступа к объектам
    locations = {
        "склад": store,
        "магазин": shop
    }

    print("=== Система доставки товаров ===")
    print("Пример: Доставить 3 печеньки из склад в магазин")
    print("Для выхода введите 'стоп' или 'выход'.\n")

    while True:
        # Вывод текущего состояния
        print_storage("склад", store)
        print_storage("магазин", shop)

        # Получение запроса от пользователя
        user_input = input("Пользователь:\n").strip()

        if user_input.lower() in ('стоп', 'выход', 'q'):
            print("\nПрограмма:\nСпасибо за использование системы доставки!")
            break

        # Парсинг запроса
        try:
            request = Request(user_input)
        except ValueError as e:
            print(f"\nПрограмма:\n{e}\n")
            continue

        from_storage = locations[request.from_point]
        to_storage = locations[request.to_point]

        print("\nПрограмма:")

        # 1. Проверка наличия товара
        source_items = from_storage.get_items()
        if request.product not in source_items:
            print(f"На {request.from_point}е нет необходимого товара, попробуйте другой запрос.\n")
            continue

        # 2. Проверка количества
        if source_items[request.product] < request.amount:
            print(f"Не хватает на {request.from_point}е, попробуйте заказать меньше.\n")
            continue

        # 3. Проверка места
        if to_storage.get_free_space() < request.amount:
            print(f"В {request.to_point}е недостаточно свободного места.\n")
            continue

        # 4. Проверка лимита уникальных товаров (только для магазина)
        if isinstance(to_storage, Shop):
            if request.product not in to_storage.get_items() and to_storage.get_unique_items_count() >= 5:
                print("В магазине уже 5 уникальных товаров, нельзя добавить новый.\n")
                continue

        # Все проверки пройдены - выполняем перемещение
        print(f"Нужное количество есть на {request.from_point}е")
        print(f"Курьер забрал {request.amount} {request.product} со {request.from_point}")
        print(f"Курьер везет {request.amount} {request.product} со {request.from_point} в {request.to_point}")

        # Изменяем состояние
        from_storage.remove(request.product, request.amount)
        to_storage.add(request.product, request.amount)

        print(f"Курьер доставил {request.amount} {request.product} в {request.to_point}\n")


if __name__ == "__main__":
    main()
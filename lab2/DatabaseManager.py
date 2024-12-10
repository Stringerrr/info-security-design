import mysql.connector
from mysql.connector import Error
from typing import List, Optional


class DatabaseManager:
    """
    Класс для управления подключением к базе данных (паттерн Одиночка).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str, user: str, password: str, database: str):
        if not hasattr(self, "_connection"):
            try:
                self._connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                self._cursor = self._connection.cursor(dictionary=True)
                print("Подключение к базе данных успешно выполнено.")
            except Error as e:
                raise Exception(f"Ошибка подключения к базе данных: {e}")

    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[dict]]:
        """
        Выполняет SQL-запрос и возвращает результат, если это SELECT.
        """
        try:
            self._cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return self._cursor.fetchall()
            else:
                self._connection.commit()
        except Error as e:
            raise Exception(f"Ошибка выполнения запроса: {e}")

    def close_connection(self):
        """Закрывает подключение к базе данных."""
        if hasattr(self, "_connection"):
            self._cursor.close()
            self._connection.close()
            print("Подключение к базе данных закрыто.")


class JewelryItemRepDB:
    """
    Класс для управления операциями с таблицей jewelry_items.
    Делегирует выполнение SQL-запросов DatabaseManager.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def get_by_id(self, item_id: int) -> Optional[dict]:
        """Получить объект по ID."""
        query = "SELECT * FROM jewelry_items WHERE item_id = %s"
        return self.db_manager.execute_query(query, (item_id,))

    def get_k_n_short_list(self, k: int, n: int) -> List[dict]:
        """Получить список k по счету n объектов."""
        start_index = (n - 1) * k
        query = "SELECT item_id, item_type, price FROM jewelry_items LIMIT %s OFFSET %s"
        return self.db_manager.execute_query(query, (k, start_index))

    def add_object(self, item: dict) -> int:
        """Добавить объект в список с формированием нового ID."""
        query = """
        INSERT INTO jewelry_items (item_type, material_id, weight, price)
        VALUES (%s, %s, %s, %s)
        """
        self.db_manager.execute_query(query, (
            item['item_type'], item['material_id'], item['weight'], item['price']
        ))
        return self.db_manager._cursor.lastrowid

    def update_object_by_id(self, item_id: int, new_data: dict):
        """Заменить элемент списка по ID."""
        query = """
        UPDATE jewelry_items
        SET item_type = %s, material_id = %s, weight = %s, price = %s
        WHERE item_id = %s
        """
        self.db_manager.execute_query(query, (
            new_data['item_type'], new_data['material_id'],
            new_data['weight'], new_data['price'], item_id
        ))

    def delete_object_by_id(self, item_id: int):
        """Удалить элемент списка по ID."""
        query = "DELETE FROM jewelry_items WHERE item_id = %s"
        self.db_manager.execute_query(query, (item_id,))

    def get_count(self) -> int:
        """Получить количество элементов."""
        query = "SELECT COUNT(*) as count FROM jewelry_items"
        result = self.db_manager.execute_query(query)
        return result[0]['count'] if result else 0


# Пример использования
if __name__ == '__main__':
    # Создание экземпляра DatabaseManager
    db_manager = DatabaseManager(
        host="93.158.134.119",
        user="root",
        password="123456",
        database="jewelry_db"
    )

    # Создание экземпляра JewelryItemRepDB с делегацией операций DatabaseManager
    repo = JewelryItemRepDB(db_manager)

    # Добавление нового объекта
    new_item_id = repo.add_object({
        "item_type": "Ring",
        "material_id": 1,
        "weight": 5.5,
        "price": 300.0
    })
    print(f"Добавлен объект с ID: {new_item_id}")

    # Получение объекта по ID
    item = repo.get_by_id(new_item_id)
    print("Полученный объект:", item)

    # Получение списка объектов
    items = repo.get_k_n_short_list(5, 1)
    print("Список объектов:", items)

    # Обновление объекта
    repo.update_object_by_id(new_item_id, {
        "item_type": "Updated Ring",
        "material_id": 1,
        "weight": 6.0,
        "price": 350.0
    })
    print("Объект обновлен.")

    # Удаление объекта
    repo.delete_object_by_id(new_item_id)
    print("Объект удален.")

    # Получение количества объектов
    count = repo.get_count()
    print("Количество объектов:", count)

    # Закрытие подключения к базе данных
    db_manager.close_connection()

import mysql.connector
from typing import List, Optional


class JewelryItemRepDB:
    def __init__(self, host: str, user: str, password: str, database: str):
        """Инициализация подключения к базе данных."""
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def get_by_id(self, item_id: int) -> Optional[dict]:
        """Получить объект по ID."""
        query = "SELECT * FROM jewelry_items WHERE item_id = %s"
        self.cursor.execute(query, (item_id,))
        result = self.cursor.fetchone()
        return result

    def get_k_n_short_list(self, k: int, n: int) -> List[dict]:
        """Получить список k по счету n объектов."""
        start_index = (n - 1) * k
        query = "SELECT item_id, item_type, price FROM jewelry_items LIMIT %s OFFSET %s"
        self.cursor.execute(query, (k, start_index))
        return self.cursor.fetchall()

    def add_object(self, item: dict) -> int:
        """Добавить объект в список с формированием нового ID."""
        query = """
        INSERT INTO jewelry_items (item_type, material_id, weight, price)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (item['item_type'], item['material_id'], item['weight'], item['price']))
        self.connection.commit()
        return self.cursor.lastrowid

    def update_object_by_id(self, item_id: int, new_data: dict):
        """Заменить элемент списка по ID."""
        query = """
        UPDATE jewelry_items
        SET item_type = %s, material_id = %s, weight = %s, price = %s
        WHERE item_id = %s
        """
        self.cursor.execute(query, (
            new_data['item_type'], 
            new_data['material_id'], 
            new_data['weight'], 
            new_data['price'], 
            item_id
        ))
        self.connection.commit()

    def delete_object_by_id(self, item_id: int):
        """Удалить элемент списка по ID."""
        query = "DELETE FROM jewelry_items WHERE item_id = %s"
        self.cursor.execute(query, (item_id,))
        self.connection.commit()

    def get_count(self) -> int:
        """Получить количество элементов."""
        query = "SELECT COUNT(*) as count FROM jewelry_items"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result['count']

    def close(self):
        """Закрыть подключение к базе данных."""
        self.cursor.close()
        self.connection.close()


# Пример использования
if __name__ == '__main__':
    # Инициализация класса с подключением к базе данных MySQL
    repo = JewelryItemRepDB(
        host="93.158.134.119",
        user="root",
        password="123456",
        database="jewelry_db"
    )

    # Добавление нового объекта
    new_item_id = repo.add_object({
        "item_type": "Necklace",
        "material_id": 3,
        "weight": 12.5,
        "price": 1500.0
    })
    print(f"Добавлен объект с ID: {new_item_id}")

    # Получение объекта по ID
    item = repo.get_by_id(new_item_id)
    print("Полученный объект:", item)

    # Получение списка элементов (например, 2-й список по 5 объектов)
    items = repo.get_k_n_short_list(5, 2)
    print("Список объектов:", items)

    # Обновление объекта
    repo.update_object_by_id(new_item_id, {
        "item_type": "Updated Necklace",
        "material_id": 3,
        "weight": 15.0,
        "price": 1600.0
    })
    print("Объект обновлен.")

    # Удаление объекта
    repo.delete_object_by_id(new_item_id)
    print("Объект удален.")

    # Получение количества элементов
    count = repo.get_count()
    print("Количество объектов в таблице:", count)

    # Закрытие подключения
    repo.close()

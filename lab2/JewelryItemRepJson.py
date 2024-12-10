import json
from typing import List, Optional

class JewelryItemRepJson:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []
        self.__load_from_file()

    def __load_from_file(self):
        """Чтение всех данных из файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError:
            raise ValueError("Ошибка чтения JSON файла. Проверьте формат данных.")

    def save_to_file(self):
        """Запись всех данных в файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def get_by_id(self, item_id: int) -> Optional[dict]:
        """Получить объект по ID."""
        return next((item for item in self.data if item['item_id'] == item_id), None)

    def get_k_n_short_list(self, k: int, n: int) -> List[dict]:
        """Получить список k по счету n объектов класса short."""
        start_index = (n - 1) * k
        return self.data[start_index:start_index + k]

    def sort_by_field(self, field: str):
        """Сортировать элементы по выбранному полю."""
        if not self.data or field not in self.data[0]:
            raise ValueError(f"Поле '{field}' отсутствует в данных.")
        self.data.sort(key=lambda x: x[field])

    def add_object(self, item: dict):
        """Добавить объект в список с формированием нового ID."""
        new_id = max((item['item_id'] for item in self.data), default=0) + 1
        item['item_id'] = new_id
        self.data.append(item)

    def update_object_by_id(self, item_id: int, new_data: dict):
        """Заменить элемент списка по ID."""
        for index, item in enumerate(self.data):
            if item['item_id'] == item_id:
                self.data[index] = {**item, **new_data, 'item_id': item_id}
                return
        raise ValueError(f"Объект с ID {item_id} не найден.")

    def delete_object_by_id(self, item_id: int):
        """Удалить элемент списка по ID."""
        self.data = [item for item in self.data if item['item_id'] != item_id]

    def get_count(self) -> int:
        """Получить количество элементов."""
        return len(self.data)


# Пример использования
if __name__ == '__main__':
    # Указываем путь к JSON-файлу
    repo = JewelryItemRepJson('jewelry_data.json')

    # Добавление объектов
    repo.add_object({"item_type": "Ring", "material_id": 1, "weight": 5.5, "price": 300.0})
    repo.add_object({"item_type": "Bracelet", "material_id": 2, "weight": 15.0, "price": 800.0})
    repo.save_to_file()

    # Получение объекта по ID
    print(repo.get_by_id(1))

    # Получение списка элементов
    print(repo.get_k_n_short_list(1, 2))  # Второй элемент

    # Сортировка по цене
    repo.sort_by_field('price')
    repo.save_to_file()

    # Обновление объекта
    repo.update_object_by_id(1, {"price": 350.0})
    repo.save_to_file()

    # Удаление объекта
    repo.delete_object_by_id(1)
    repo.save_to_file()

    # Количество элементов
    print("Количество элементов:", repo.get_count())

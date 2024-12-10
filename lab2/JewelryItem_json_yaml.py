import json
import yaml
from typing import List, Optional


class JewelryItemRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []
        self.__load_from_file()

    def __load_from_file(self):
        """Чтение всех данных из файла (переопределяется в дочерних классах)."""
        raise NotImplementedError("Этот метод должен быть переопределён в дочернем классе.")

    def save_to_file(self):
        """Запись всех данных в файл (переопределяется в дочерних классах)."""
        raise NotImplementedError("Этот метод должен быть переопределён в дочернем классе.")

    def get_by_id(self, item_id: int) -> Optional[dict]:
        """Получить объект по ID."""
        return next((item for item in self.data if item['item_id'] == item_id), None)

    def get_k_n_short_list(self, k: int, n: int) -> List[dict]:
        """Получить список k по счету n объектов."""
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


class JewelryItemRepJson(JewelryItemRepository):
    def __load_from_file(self):
        """Чтение всех данных из JSON-файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = []
        except json.JSONDecodeError:
            raise ValueError("Ошибка чтения JSON файла. Проверьте формат данных.")

    def save_to_file(self):
        """Запись всех данных в JSON-файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)


class JewelryItemRepYaml(JewelryItemRepository):
    def __load_from_file(self):
        """Чтение всех данных из YAML-файла."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file) or []
        except FileNotFoundError:
            self.data = []
        except yaml.YAMLError:
            raise ValueError("Ошибка чтения YAML файла. Проверьте формат данных.")

    def save_to_file(self):
        """Запись всех данных в YAML-файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.data, file, allow_unicode=True, default_flow_style=False)


# Пример использования
if name == '__main__':
    # Работа с JSON
    json_repo = JewelryItemRepJson('jewelry_data.json')
    json_repo.add_object({"item_type": "Ring", "material_id": 1, "weight": 5.5, "price": 300.0})
    json_repo.save_to_file()

    # Работа с YAML
    yaml_repo = JewelryItemRepYaml('jewelry_data.yaml')
    yaml_repo.add_object({"item_type": "Bracelet", "material_id": 2, "weight": 15.0, "price": 800.0})
    yaml_repo.save_to_file()

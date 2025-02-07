import yaml
import json

class BaseGoldRep:
    def __init__(self, name, cost, size, SKU, item_id=None):
        self._name = self.validate_name(name)
        self._cost = self.validate_cost(cost)
        self._size = self.validate_size(size)
        self._SKU = self.validate_SKU(SKU)
        self._item_id = item_id
    
    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or not name:
            raise ValueError("Некорректное имя.")
        return name
    
    @staticmethod
    def validate_cost(cost):
        if not isinstance(cost, (int, float)) or cost <= 0:
            raise ValueError("Цена должна быть положительным числом.")
        return cost
    
    @staticmethod
    def validate_size(size):
        if not isinstance(size, (int, float)) or size <= 0:
            raise ValueError("Размер должен быть положительным числом.")
        return size
    
    @staticmethod
    def validate_SKU(SKU):
        if not isinstance(SKU, int) or SKU <= 0:
            raise ValueError("SKU должен быть положительным целым числом.")
        return SKU
    
    def __eq__(self, other):
        return isinstance(other, BaseGoldRep) and self._SKU == other._SKU
    
    def __str__(self):
        return f"Полная версия: {self.__dict__}"
    
    def short_version(self):
        return f"Кратко: {self._name}, Цена: {self._cost}"
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

class GoldRepYaml:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                raw_data = yaml.safe_load(file) or []
                self.data = [BaseGoldRep(**item) for item in raw_data]
        except FileNotFoundError:
            print("Файл не найден, начинаем с пустого списка.")
            self.data = []
        except Exception as e:
            print("Ошибка при чтении YAML файла:", e)
            self.data = []

    def save_to_file(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                yaml.dump([obj.__dict__ for obj in self.data], file, allow_unicode=True)
        except Exception as e:
            print("Ошибка при записи YAML файла:", e)

    def get_by_id(self, item_id):
        for item in self.data:
            if item._item_id == item_id:
                return item
        print(f"Объект с ID {item_id} не найден.")
        return None

    def get_k_n_short_list(self, k, n):
        start_index = (n - 1) * k
        end_index = start_index + k
        if start_index >= len(self.data):
            print("Неверный номер страницы.")
            return []
        return [item.short_version() for item in self.data[start_index:end_index]]

    def sort_by_field(self, field='_name'):
        try:
            self.data.sort(key=lambda x: getattr(x, field, '').lower())
        except Exception as e:
            print(f"Ошибка при сортировке по полю {field}:", e)

    def add_object(self, item):
        if not isinstance(item, dict):
            print("Ошибка: объект должен быть словарем.")
            return
        try:
            new_id = max((obj._item_id or 0 for obj in self.data), default=0) + 1
            new_obj = BaseGoldRep(**item, item_id=new_id)
            self.data.append(new_obj)
        except Exception as e:
            print("Ошибка при добавлении объекта:", e)

    def update_object_by_id(self, item_id, new_data):
        for item in self.data:
            if item._item_id == item_id:
                for key, value in new_data.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                return
        print(f"Объект с ID {item_id} не найден.")

    def delete_object_by_id(self, item_id):
        for i, item in enumerate(self.data):
            if item._item_id == item_id:
                del self.data[i]
                return
        print(f"Объект с ID {item_id} не найден для удаления.")

    def get_count(self):
        return len(self.data)

if __name__ == '__main__':
    fl = GoldRepYaml("data.yaml")

    fl.add_object({"name": "Ring", "cost": 100, "size": 16, "SKU": 1061})
    fl.add_object({"name": "Chain", "cost": 400, "size": 45, "SKU": 1062})
    fl.save_to_file()

    print(fl.get_by_id(1))
    print(fl.get_k_n_short_list(1, 1))

    fl.sort_by_field("_name")
    fl.save_to_file()

    fl.update_object_by_id(1, {"_cost": 150})
    fl.save_to_file()

    fl.delete_object_by_id(2)
    fl.save_to_file()

    print("Количество объектов:", fl.get_count())

import json
import yaml

class GoldRepBase:
    def __init__(self, file_path=None, data=None):
        self.__file_path = golddb.json
        self.__data = data if data is not None else []

    # Инкапсуляция
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        self.__file_path = value

    # Валидация
    @staticmethod
    def validate_object(item):
        if not isinstance(item, dict):
            raise ValueError("Объект должен быть словарем")
        if "name" not in item or "cost" not in item:
            raise ValueError("Объект должен содержать поля 'name' и 'cost'")
        if not isinstance(item['name'], str) or not isinstance(item['cost'], (int, float)):
            raise ValueError("'name' должен быть строкой, а 'cost' числом")

    def load_from_file(self):
        raise NotImplementedError("Ошибка")

    def save_to_file(self):
        raise NotImplementedError("Ошибка")

    def get_by_id(self, item_id):
        for item in self.data:
            if item.get('item_id') == item_id:
                return item
        print(f"Объект с ID {item_id} не найден")
        return None

    def get_k_n_short_list(self, k, n):
        start_index = (n - 1) * k
        end_index = start_index + k
        if start_index >= len(self.data):
            print("Неверный номер страницы")
            return []
        return self.data[start_index:end_index]

    def sort_by_field(self, field):
        try:
            self.data.sort(key=lambda x: x[field])
        except KeyError:
            print(f"Поле {field} отсутствует в данных")

    def add_object(self, item):
        try:
            self.validate_object(item)
        except ValueError as e:
            print(f"Ошибка: {e}")
            return

        try:
            new_id = max([obj['item_id'] for obj in self.data]) + 1
        except ValueError:
            new_id = 1
        item['item_id'] = new_id
        self.data.append(item)

    def update_object_by_id(self, item_id, new_data):
        for item in self.data:
            if item['item_id'] == item_id:
                item.update(new_data)
                return
        print(f"Объект с ID {item_id} не найден")

    def delete_object_by_id(self, item_id):
        for item in self.data:
            if item['item_id'] == item_id:
                self.data.remove(item)
                return
        print(f"Объект с ID {item_id} не найден для удаления")

    def get_count(self):
        return len(self.data)

    def __str__(self):
        return f"Полная версия объекта: {self.data}"

    def __repr__(self):
        return f"Краткая версия объекта: {self.get_k_n_short_list(5, 1)}"

    def __eq__(self, other):
        if not isinstance(other, GoldRepBase):
            return False
        return self.data == other.data


class GoldRepJson(GoldRepBase):
    def __init__(self, file_path=None, data=None):
        super().__init__(file_path, data)

    def load_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("Файл не найден. Начинаем с пустого списка")
            self.data = []
        except:
            print("Произошла ошибка при чтении JSON файла")
            self.data = []

    def save_to_file(self):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
        except:
            print("Ошибка при сохранении JSON файла")


class GoldRepYaml(GoldRepBase):
    def __init__(self, file_path=None, data=None):
        super().__init__(file_path, data)

    def load_from_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file) or []
        except FileNotFoundError:
            print("Файл не найден. Начинаем с пустого списка")
            self.data = []
        except:
            print("Произошла ошибка при чтении YAML файла")
            self.data = []

    def save_to_file(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.data, file, allow_unicode=True, default_flow_style=False)
        except:
            print("Ошибка при сохранении YAML файла")

if __name__ == '__main__':
    fl_json = GoldRepJson("file.json")
    fl_yaml = GoldRepYaml("file.yaml")

    fl_json.add_object({"name": "Ring", "cost": 100})
    fl_yaml.add_object({"name": "Chain", "cost": 400})

    fl_json.save_to_file()
    fl_yaml.save_to_file()

    fl_json.load_from_file()
    fl_yaml.load_from_file()

    print("Получаем объект по ID из JSON:")
    print(fl_json.get_by_id(1))
    print("Получаем объект по ID из YAML:")
    print(fl_yaml.get_by_id(1))

    print("\nПолная версия данных JSON:")
    print(fl_json)
    print("Полная версия данных YAML:")
    print(fl_yaml)

    print("\nКраткая версия данных JSON:")
    print(fl_json.__repr__())
    print("Краткая версия данных YAML:")
    print(fl_yaml.__repr__())

    fl_json.sort_by_field("name")
    fl_yaml.sort_by_field("name")

    print("\nДанные JSON после сортировки по имени:")
    print(fl_json)
    print("Данные YAML после сортировки по имени:")
    print(fl_yaml)

    print("\nКраткий список JSON (1-я страница, 2 объекта):")
    print(fl_json.get_k_n_short_list(2, 1))
    print("Краткий список YAML (1-я страница, 2 объекта):")
    print(fl_yaml.get_k_n_short_list(2, 1))

    fl_json.update_object_by_id(1, {"name": "Gold Ring", "cost": 120})
    fl_yaml.update_object_by_id(1, {"name": "Gold Chain", "cost": 450})

    print("\nДанные JSON после обновления:")
    print(fl_json.get_by_id(1))
    print("Данные YAML после обновления:")
    print(fl_yaml.get_by_id(1))

    fl_json.delete_object_by_id(1)
    fl_yaml.delete_object_by_id(1)

    print("\nДанные JSON после удаления:")
    print(fl_json.get_by_id(1))
    print("Данные YAML после удаления:")
    print(fl_yaml.get_by_id(1))

    print("\nКоличество объектов в JSON:", fl_json.get_count())
    print("Количество объектов в YAML:", fl_yaml.get_count())

    json_copy = GoldRepJson("file.json")
    json_copy.add_object({"name": "Ring", "cost": 100})
    print("\nРавенство объектов JSON:")
    print(fl_json == json_copy)
    print(fl_json == fl_yaml)


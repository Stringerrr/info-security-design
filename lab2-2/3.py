import json
import yaml

class GoldRepBase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

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
        if not isinstance(item, dict):
            print("Ошибка. Объект должен быть словарем")
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

class GoldRepJson(GoldRepBase):
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
    repo_json = GoldRepJson("file.json")
    repo_json.add_object({"name": "Ring", "cost": 100})
    repo_json.save_to_file()
    print(repo_json.get_by_id(1))

    repo_yaml = GoldRepYaml("file.yaml")
    repo_yaml.add_object({"name": "Chain", "cost": 400})
    repo_yaml.save_to_file()
    print(repo_yaml.get_by_id(1))

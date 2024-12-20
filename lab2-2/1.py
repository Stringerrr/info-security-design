import json

class MyEntityRepJson:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("Файл не найден, начинаем с пустого списка.")
            self.data = []
        except:
            print("Произошла ошибка при чтении файла.")
            self.data = []

    def save_to_file(self):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
        except:
            print("Не удалось сохранить файл.")

    def get_by_id(self, item_id):
        for item in self.data:
            if item.get('item_id') == item_id:
                return item
        print(f"Объект с ID {item_id} не найден.")
        return None

    def get_k_n_short_list(self, k, n):
        start_index = (n - 1) * k
        end_index = start_index + k
        if start_index >= len(self.data):
            print("Неверный номер страницы.")
            return []
        return self.data[start_index:end_index]

    def sort_by_field(self, field):
        try:
            self.data.sort(key=lambda x: x[field])
        except KeyError:
            print(f"Поле {field} отсутствует в данных.")

    def add_object(self, item):
        if not isinstance(item, dict):
            print("Ошибка: объект должен быть словарем.")
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
        print(f"Объект с ID {item_id} не найден.")

    def delete_object_by_id(self, item_id):
        for item in self.data:
            if item['item_id'] == item_id:
                self.data.remove(item)
                return
        print(f"Объект с ID {item_id} не найден для удаления.")

    def get_count(self):
        return len(self.data)

if __name__ == '__main__':
    repo = MyEntityRepJson("file.json")

    repo.add_object({"name": "Ring", "cost": 100})
    repo.add_object({"name": "Chain", "cost": 400})
    repo.save_to_file()

    print(repo.get_by_id(1))
    print(repo.get_k_n_short_list(1, 1))

    repo.sort_by_field("cost")
    repo.save_to_file()

    repo.update_object_by_id(1, {"cost": 150})
    repo.save_to_file()

    repo.delete_object_by_id(2)
    repo.save_to_file()

    print("Количество объектов:", repo.get_count())

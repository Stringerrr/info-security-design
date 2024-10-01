import json


class JewelryItem:
    def __init__(self, item_id: int, item_type: str, material_id: int, weight: float, price: float):
        self.__item_id = self.__validate(item_id, int, positive=True)
        self.__item_type = self.__validate(item_type, str, non_empty=True) 
        self.__material_id = self.__validate(material_id, int, positive=True) 
        self.__weight = self.__validate(weight, (float, int), positive=True) 
        self.__price = self.__validate(price, (float, int), non_negative=True) 

    @staticmethod
    def __validate(value, value_type, positive=False, non_empty=False, non_negative=False):
        if not isinstance(value, value_type):
            raise ValueError(f"Значение должно быть типа {value_type.__name__}.")

        if positive and (value <= 0):
            raise ValueError("Значение должно быть положительным.")

        if non_empty and (value == ""):
            raise ValueError("Значение не должно быть пустой строкой.")

        if non_negative and (value < 0):
            raise ValueError("Значение должно быть неотрицательным.")

        return value if not isinstance(value, (float, int)) else float(value)

    # Перегрузка конструктора для строки
    @classmethod
    def from_string(cls, data: str):
        parts = data.split(',')
        if len(parts) != 5:
            raise ValueError("Строка должна содержать 5 частей, разделенных запятыми.")

        item_id = int(parts[0].strip())
        item_type = parts[1].strip()
        material_id = int(parts[2].strip())
        weight = float(parts[3].strip())
        price = float(parts[4].strip())

        return cls(item_id, item_type, material_id, weight, price)

    # Перегрузка конструктора для JSON
    @classmethod
    def from_json(cls, json_data: str):
        data = json.loads(json_data)
        return cls(
            item_id=data['item_id'],
            item_type=data['item_type'],
            material_id=data['material_id'],
            weight=data['weight'],
            price=data['price']
        )


    def get_item_id(self) -> int:
        return self.__item_id

    def get_item_type(self) -> str:
        return self.__item_type

    def get_material_id(self) -> int:
        return self.__material_id

    def get_weight(self) -> float:
        return self.__weight

    def get_price(self) -> float:
        return self.__price


    def set_item_type(self, item_type: str):
        self.__item_type = self.__validate(item_type, str, non_empty=True)

    def set_material_id(self, material_id: int):
        self.__material_id = self.__validate(material_id, int, positive=True)

    def set_weight(self, weight: float):
        self.__weight = self.__validate(weight, (float, int), positive=True)

    def set_price(self, price: float):
        self.__price = self.__validate(price, (float, int), non_negative=True)

    def __str__(self) -> str:
        return (f"JewelryItem(id={self.__item_id}, type={self.__item_type}, "
                f"material_id={self.__material_id}, weight={self.__weight}, price={self.__price})")



try:
    # Создание объекта с использованием конструктора
    jewelry_item = JewelryItem(item_id=1, item_type="Ring", material_id=101, weight=10.5, price=250.0)
    print(jewelry_item)

    # Создание объекта из строки
    jewelry_item_from_string = JewelryItem.from_string("2, Necklace, 102, 15.0, 300.0")
    print(jewelry_item_from_string)

    # Создание объекта из JSON
    json_data = '{"item_id": 3, "item_type": "Bracelet", "material_id": 103, "weight": 20.0, "price": 400.0}'
    jewelry_item_from_json = JewelryItem.from_json(json_data)
    print(jewelry_item_from_json)


    invalid_jewelry_item = JewelryItem(item_id=-1, item_type="", material_id=0, weight=-5, price=-50)
except ValueError as e:
    print(f"Ошибка создания объекта: {e}")

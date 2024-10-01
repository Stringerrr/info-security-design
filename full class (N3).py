class JewelryItem:
    def __init__(self, item_id: int, item_type: str, material_id: int, weight: float, price: float):
        self.__item_id = item_id        # Первичный ключ
        self.__item_type = item_type    # Тип изделия
        self.__material_id = material_id # Внешний ключ, ссылается на материал
        self.__weight = weight          # Вес изделия в граммах
        self.__price = price            # Стоимость изделия

    # Геттеры
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

    # Сеттеры
    def set_item_type(self, item_type: str):
        self.__item_type = item_type

    def set_material_id(self, material_id: int):
        self.__material_id = material_id

    def set_weight(self, weight: float):
        self.__weight = weight

    def set_price(self, price: float):
        self.__price = price

    def __str__(self) -> str:
        return f"JewelryItem(id={self.__item_id}, type={self.__item_type}, material_id={self.__material_id}, weight={self.__weight}, price={self.__price})"

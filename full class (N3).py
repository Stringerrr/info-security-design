class JewelryItem:
    def __init__(self, item_id: int, item_type: str, material_id: int, weight: float, price: float):
        self.__item_id = item_id
        self.__item_type = item_type
        self.__material_id = material_id
        self.__weight = weight
        self.__price = price

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


jewelry_item = JewelryItem(item_id=1, item_type="Ring", material_id=101, weight=10.5, price=250.0)

print(jewelry_item)

jewelry_item.set_item_type("Bracelet")
print(jewelry_item.get_item_type())

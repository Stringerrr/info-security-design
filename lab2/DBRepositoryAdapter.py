class DBRepositoryAdapter(JewelryItemRepository):
    def __init__(self, host: str, user: str, password: str, database: str):
        super().__init__(None)  # filename здесь не нужен, так как используется база данных
        self.db_manager = JewelryItemRepDB(
            DatabaseManager(host, user, password, database)
        )

    def load_entities(self):
        """Загрузка данных из базы данных — адаптируем под общий интерфейс"""
        query = "SELECT * FROM jewelry_items"
        self.data = self.db_manager.db_manager.execute_query(query)

    def save_entities(self):
        pass

    def get_by_id(self, item_id: int) -> Optional[dict]:
        """Получить объект по ID через JewelryItemRepDB"""
        return self.db_manager.get_by_id(item_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[dict]:
        """Получить список k по счету n объектов через JewelryItemRepDB"""
        return self.db_manager.get_k_n_short_list(k, n)

    def add_object(self, item: dict):
        """Добавить объект в базу данных через JewelryItemRepDB"""
        return self.db_manager.add_object(item)

    def replace_entity_by_id(self, item_id: int, updated_item: dict):
        """Обновить объект в базе данных через JewelryItemRepDB"""
        self.db_manager.update_object_by_id(item_id, updated_item)

    def delete_object_by_id(self, item_id: int):
        """Удалить объект по ID через JewelryItemRepDB"""
        self.db_manager.delete_object_by_id(item_id)

    def get_count(self) -> int:
        """Получить количество объектов через JewelryItemRepDB"""
        return self.db_manager.get_count()

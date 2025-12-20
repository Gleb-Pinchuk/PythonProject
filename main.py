from src.app import load_data_to_db
from src.config import load_db_config, get_db_name
from src.db_manager import DBManager
from src.ui import show_analysis


def main() -> None:
    config = load_db_config()
    db_name = get_db_name()

    print("🔄 Загрузка данных из hh.ru и сохранение в PostgreSQL...")
    load_data_to_db(db_name, config)

    print("✅ Данные успешно загружены. Анализ:")
    db = DBManager(db_name, config)
    show_analysis(db)


if __name__ == "__main__":
    main()

from store_telega.bd import connect_to_db


def create_db() -> None:
    """Создаёт базу данных"""

    # Подключение к базе данных
    with connect_to_db() as connection:

        # Создание курсора
        cursor = connection.cursor()

        # Создание таблицы 'employees'
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS zuzu ( id INTEGER PRIMARY KEY, title TEXT NOT NULL, url TEXT NOT NULL, price DECIMAL ); """
        )
    return None


def add_data(title: str, url: str, price: float) -> bool:
    """
    Добавляет запись в базу данных
    """

    data = [
        (title, url, price),
    ]
    # Подключение к базе данных
    with connect_to_db() as connection:

        # Создание курсора
        cursor = connection.cursor()

        # Вставка записи в таблицу
        cursor.executemany(
            "INSERT INTO zuzu (title, url, price) VALUES (?, ?, ?)", data
        )

        # Сохранение изменений в базу данных
        connection.commit()

    return True

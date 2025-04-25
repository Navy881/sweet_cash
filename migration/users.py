
import os
import psycopg2
from dotenv import load_dotenv


load_dotenv(os.path.join('local.env'))

POSTGRESQL_USER: str = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD: str = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_SERVER: str = os.getenv("POSTGRESQL_SERVER")
POSTGRESQL_PORT: str = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DATABASE: str = os.getenv("POSTGRESQL_DATABASE")


SRC_DB_CONFIG = {
    "host": POSTGRESQL_SERVER,
    "port": POSTGRESQL_PORT,
    "database": POSTGRESQL_DATABASE,
    "user": POSTGRESQL_USER,
    "password": POSTGRESQL_PASSWORD
}

DST_DB_CONFIG = {
    "host": POSTGRESQL_SERVER,
    "port": POSTGRESQL_PORT,
    "database": "sc_users",
    "user": POSTGRESQL_USER,
    "password": POSTGRESQL_PASSWORD
}

SELECT_QUERY = """
    SELECT 
        id,
        created_at AT TIME ZONE 'UTC' AS created_at,
        COALESCE(
            updated_at AT TIME ZONE 'UTC', 
            created_at AT TIME ZONE 'UTC'
        ) AS updated_at,
        name,
        email,
        phone,
        password,
        COALESCE(confirmed, FALSE) AS confirmed,
        deleted AT TIME ZONE 'UTC' AS deleted
    FROM public.users
"""

INSERT_QUERY = """
    INSERT INTO public.users (
        id,
        created_at,
        updated_at,
        name,
        email,
        phone,
        password,
        confirmed,
        deleted
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
"""

UPDATE_SEQUENCE = """
    SELECT setval('users_id_seq', (SELECT MAX(id) FROM public.users));
"""


def migrate_data():
    try:
        with psycopg2.connect(**SRC_DB_CONFIG) as src_conn:
            with src_conn.cursor() as src_cursor:
                print("Получение данных из исходной таблицы...")
                src_cursor.execute(SELECT_QUERY)
                data = src_cursor.fetchall()
                print(f"Найдено {len(data)} записей")

        with psycopg2.connect(**DST_DB_CONFIG) as dst_conn:
            with dst_conn.cursor() as dst_cursor:
                print("Вставка данных в целевую таблицу...")
                dst_cursor.executemany(INSERT_QUERY, data)

                print("Обновление последовательности ID...")
                dst_cursor.execute(UPDATE_SEQUENCE)

                dst_conn.commit()
                print("Миграция успешно завершена!")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if 'dst_conn' in locals():
            dst_conn.rollback()


if __name__ == "__main__":
    migrate_data()
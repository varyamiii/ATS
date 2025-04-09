# request.py

import psycopg2
from psycopg2 import sql

class DatabaseHandler:
    def __init__(self, db_config):
        self.connection = None
        try:
            self.connection = psycopg2.connect(**db_config)
            print("Подключение к базе данных установлено.")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто.")

    def insert_position(self, position_data):
        query = sql.SQL("""
            INSERT INTO job_positions (
                position_name, competency_level, employment_type, education,
                work_experience, key_skills, english_level, special_requirements
            ) VALUES (
                %(position_name)s, %(competency_level)s, %(employment_type)s, %(education)s,
                %(work_experience)s, %(key_skills)s, %(english_level)s, %(special_requirements)s
            )
        """)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, position_data)
                self.connection.commit()
                print("Запись успешно добавлена.")
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка при добавлении записи: {e}")
            raise
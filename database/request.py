# request.py

import psycopg2
from psycopg2 import sql

# # Конфигурация базы данных
# DB_CONFIG = {
#     'dbname': 'hh_helper',
#     'user': 'postgres',
#     'password': 'wolf24aravrav050504',
#     'host': 'localhost',
#     'port': 5432
# }

from dotenv import load_dotenv
import os
load_dotenv()

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),  # Без значения по умолчанию
    'user': os.getenv('DB_USER'),    # Без значения по умолчанию
    'password': os.getenv('DB_PASSWORD'),  # Без значения по умолчанию
    'host': os.getenv('DB_HOST'),    # Без значения по умолчанию
    'port': (os.getenv('DB_PORT'))  # Без значения по умолчанию
}

# Проверка загруженных переменных окружения
print("DB_NAME:", os.getenv('DB_NAME'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_PORT:", os.getenv('DB_PORT'))


class DatabaseHandler:
    def __init__(self):
        self.connection = None
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
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

    def insert_candidate(self, candidate_data, resume_path):
        query = sql.SQL("""
            INSERT INTO candidates (
                full_name, phone, email, skills, english_level, education, work_experience, resume
            ) VALUES (
                %(full_name)s, %(phone)s, %(email)s, %(skills)s, %(english_level)s, %(education)s, %(work_experience)s, %(resume)s
            )
        """)

        try:
            # Чтение PDF-файла в бинарном формате
            with open(resume_path, "rb") as file:
                resume_data = file.read()

            # Добавляем бинарные данные в словарь candidate_data
            candidate_data["resume"] = psycopg2.Binary(resume_data)

            with self.connection.cursor() as cursor:
                cursor.execute(query, candidate_data)
                self.connection.commit()
                print("Кандидат успешно добавлен в базу данных.")
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка при добавлении кандидата: {e}")
            raise

#=================================Считывание бинарного файла в PDF из БД================

# def fetch_resume(candidate_id, output_path):
#     try:
#         # Подключение к базе данных
#         connection = psycopg2.connect(**DB_CONFIG)
#         cursor = connection.cursor()
#
#         # Выполнение запроса для получения PDF-файла
#         query = "SELECT resume FROM candidates WHERE id = %s"
#         cursor.execute(query, (candidate_id,))
#         result = cursor.fetchone()
#
#         if result and result[0]:
#             # Извлечение бинарных данных
#             resume_data = result[0]
#
#             # Сохранение данных в файл
#             with open(output_path, "wb") as file:
#                 file.write(resume_data)
#
#             print(f"PDF-файл успешно сохранен: {output_path}")
#         else:
#             print("Резюме не найдено для данного ID.")
#
#     except Exception as e:
#         print(f"Ошибка при извлечении резюме: {e}")
#
#     finally:
#         # Закрытие соединения
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()
#
# # Пример использования
# candidate_id = 1  # ID кандидата
# output_path = "downloaded_resume.pdf"  # Путь для сохранения файла
# fetch_resume(candidate_id, output_path)
from app import app  # Импортируем FastAPI приложение
import uvicorn
from database.base import init_db

# Тестовое подключение к базе данных
def test_connection():
    try:
        # Используем синхронный драйвер psycopg2 для тестового подключения
        import psycopg2
        conn = psycopg2.connect(
            user="root",
            password="sqlritach",
            database="candidate_selection",
            host="localhost",
            port=5432
        )
        print("Подключение успешно!")
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

# Точка входа в приложение
def main():
    #
    # # Инициализация базы данных
    # init_db()
    # print("База данных инициализирована.")

    # Запуск сервера
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    try:
        print("Запуск сервера...")
        server.run()
    except KeyboardInterrupt:
        print("Сервер остановлен")

if __name__ == "__main__":
    try:

        main()




    except KeyboardInterrupt:
        print("Приложение выключено")
from app import app  # Импортируем FastAPI приложение
import uvicorn

# Тестовое подключение к базе данных

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
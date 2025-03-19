import asyncio
from app import app  # Импортируем FastAPI приложение
import uvicorn
#------------------------точка входа в приложение
async def main():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    try:
        print("Запуск сервера...")
        await server.serve()
    except KeyboardInterrupt:
        print("Сервер остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Приложение выключено")
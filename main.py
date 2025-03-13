import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# Создаем экземпляр FastAPI
app = FastAPI()


# Подключение папки static для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настройка Jinja2 для работы с шаблонами
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    """
    Страница авторизации администратора.
    Отображает HTML-шаблон base.html.
    """
    # Рендеринг шаблона с передачей объекта запроса
    return templates.TemplateResponse("base.html", {"request": request})

async def main():
    # Настройка и запуск сервера через uvicorn
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)

    try:
        print("Запуск сервера...")
        await server.serve()
    except KeyboardInterrupt:
        print("Сервер остановлен")
        print('lalala')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Приложение выключено")
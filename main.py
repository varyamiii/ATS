import asyncio
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import os
import json

os.environ["hf_disable_symlimks"] = "1"

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
model = SentenceTransformer('all-MiniLM-L6-v2')
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        # Проверка расширения файла
        if not file.filename.lower().endswith('.pdf'):
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": "Недопустимый формат файла. Разрешены только PDF."
            })
            continue

        try:
            # Сохранение файла
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Извлечение текста (теперь ВКЛЮЧЕНО)
            text = extract_text_from_pdf(file_path)

            # Создание эмбеддинга (теперь ВКЛЮЧЕНО)
            embedding = model.encode(text)
            embedding_path = os.path.join(UPLOAD_FOLDER, f"{file.filename}.json")
            with open(embedding_path, "w", encoding="utf-8") as f:
                json.dump({
                    "filename": file.filename,
                    "embedding": embedding.tolist()
                }, f, ensure_ascii=False, indent=4)

            results.append({
                "filename": file.filename,
                "status": "success",
                "message": "Текст успешно извлечен и обработан.",
                "text": text[:100] + "...",
                "embedding_path": embedding_path
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": f"Ошибка: {str(e)}"
            })

    return {"results": results}

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

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
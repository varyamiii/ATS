# app/routes.py
from fastapi import APIRouter, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from app.utils import extract_text_from_pdf
from app.models import process_embedding
import os
import json
#------------------------Маршруты API
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.post("/upload")
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
            file_path = os.path.join("uploads", file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Извлечение текста
            text = extract_text_from_pdf(file_path)

            # Создание эмбеддинга
            embedding_path = os.path.join("uploads", f"{file.filename}.json")
            embedding_result = process_embedding(text, embedding_path)

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
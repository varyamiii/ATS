# app/routes.py
from fastapi import APIRouter, Request, File, UploadFile, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import db

from app.utils import extract_text_from_pdf, save_text_to_json, parse_resume, \
    extract_entities, lemmatize_text, clean_text, tokenize_text, create_vector, \
    process_contact_info, process_personal_info, process_education, \
    process_skills, extract_english_level, load_universities
from app.models import process_embedding
import os
import json

from database.request import DatabaseHandler

#------------------------Маршруты API
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    #db: AsyncSession = Depends(get_db)
    results = []
    db_handler = DatabaseHandler()

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
            # universities = load_universities("uni.txt")
            # print(universities)
            # Извлечение текста
            text = extract_text_from_pdf(file_path)

            person=process_personal_info(text)
            phone_email=process_contact_info(text)
            skills=process_skills(text)
            english= extract_english_level(text)
            # Разбор контактов
            phone = phone_email.get('phone', '').strip()
            email = phone_email.get('email', '').strip()

            # print(text)
            # print("Извлеченный текст:", text[:500])
            print("Сущности:", extract_entities(text))
            # print("лема:", lemmatize_text(text))
            # print("токены:", tokenize_text(text))
            # print("образование:", process_education(text, universities))
            print("человек :", process_personal_info(text))
            print(("контакты :",process_contact_info(text)))
            print("навыки :",process_skills(text))

            print("уровень английского : ",extract_english_level(text))
            # print("навыки2.0", process_skills(text))


            # Сохранение текста в JSON
            json_output_path = os.path.join("uploads", f"{os.path.splitext(file.filename)[0]}.json")
            save_text_to_json(text, json_output_path)

            blocks = parse_resume(text)
            print(blocks)
            # # Добавление кандидата в базу данных
            # new_candidate = await add_candidate_to_db(db, blocks, text)

            # Подготовка данных для вставки
            candidate_data = {
                "full_name": person.get('name', ''),  # ФИО
                "phone": phone,  # Телефон
                "email": email,  # Почта
                "skills": skills,  # Навыки (массив строк)
                "english_level": english,  # Уровень английского
                "education": "",  # Пустое поле для образования
                "work_experience": ""  # Пустое поле для опыта работы
            }

            # Вставка данных в таблицу candidates вместе с PDF-файлом
            db_handler.insert_candidate(candidate_data, file_path)
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
    db_handler.close_connection()
    return {"results": results}


@router.post("/add_position")
async def add_position(position_data: dict):
    try:
        # Создаем объект для работы с базой данных
        db_handler = DatabaseHandler()

        # Добавляем данные в базу
        db_handler.insert_position(position_data)

        return {"message": "Данные успешно добавлены в базу данных!"}
    except Exception as e:
        return {"error": str(e)}, 500
@router.get("/ranking")
async def show_ranking(request: Request, position: str = ""):
    return templates.TemplateResponse(
        "ranking.html",
        {
            "request": request,
            "position": position
        }
    )

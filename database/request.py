from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.base import Candidate

def add_candidate_to_db(db: Session, blocks: dict, text: str):
    """
    Формирует данные для записи в БД и добавляет нового кандидата.
    :param db: Синхронная сессия базы данных.
    :param blocks: Словарь с разобранными блоками текста резюме.
    :param text: Полный текст резюме.
    :return: Созданный объект Candidate или None в случае ошибки.
    """
    try:
        # Формирование данных для записи в БД
        candidate_data = {
            "name": blocks.get("personal_info", {}).get("name"),
            "email": blocks.get("contact_info", {}).get("email"),
            "phone": blocks.get("contact_info", {}).get("phone"),
            "employment_type": None,  # Можно извлечь из текста или задать по умолчанию
            "work_format": None,  # Можно извлечь из текста или задать по умолчанию
            "education": blocks.get("education", {}).get("university"),
            "skills": blocks.get("skills", []),
            "experience_years": None,  # Можно извлечь из текста или задать по умолчанию
            "english_level": None,  # Можно извлечь из текста или задать по умолчанию
            "special_requirements": blocks.get("projects"),
            "resume_text": text
        }

        # Добавление кандидата в базу данных
        new_candidate = Candidate(**candidate_data)
        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)

        return new_candidate

    except SQLAlchemyError as e:
        # Логирование ошибки
        print(f"Ошибка при добавлении кандидата в БД: {e}")
        db.rollback()  # Откат транзакции в случае ошибки
        return None
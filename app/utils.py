from PyPDF2 import PdfReader
import json
import re
import spacy
#-----------------------------Вспомогательные функции для работы с PDF.

#извлечение текста с pdf
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Если текст не найден, добавляем пустую строку
    return text

# Функция для сохранения текста в JSON
def save_text_to_json(text, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"text": text}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise IOError(f"Ошибка при записи JSON: {e}")


#----------------------------Предобработка текста

# Загрузка модели spaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

def parse_resume(text):
    blocks = {}

    # Разбиение текста на блоки с помощью регулярных выражений
    def extract_block(pattern, text):
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else None

    # Контактная информация
    contact_info = extract_block(r"(?i)(?:контакты|contact info):\s*(.*?)(\n\n|\Z)", text)
    if contact_info:
        blocks["contact_info"] = process_contact_info(contact_info)

    # Личная информация
    personal_info = extract_block(r"(?i)(?:личная информация|personal info):\s*(.*?)(\n\n|\Z)", text)
    if personal_info:
        blocks["personal_info"] = process_personal_info(personal_info)

    # Образование
    education = extract_block(r"(?i)(?:образование|education):\s*(.*?)(\n\n|\Z)", text)
    if education:
        blocks["education"] = process_education(education)

    # Курсы и тренинги
    courses = extract_block(r"(?i)(?:курсы и тренинги|courses and training|Professional development):\s*(.*?)(\n\n|\Z)", text)
    if courses:
        blocks["courses"] = courses.strip()

    # Проекты
    projects = extract_block(r"(?i)(?:проекты|pet-project):\s*(.*?)(\n\n|\Z)", text)
    if projects:
        blocks["projects"] = projects.strip()

    # Навыки
    skills = extract_block(r"(?i)(?:навыки|skills|технические навыки|stack|Technical Skills):\s*(.*?)(\n\n|\Z)", text)
    if skills:
        blocks["skills"] = process_skills(skills)

    # Личные качества
    qualities = extract_block(r"(?i)(?:личные качества|personal qualities):\s*(.*?)(\n\n|\Z)", text)
    if qualities:
        blocks["qualities"] = qualities.strip()

    return blocks


# Дополнительные функции для обработки блоков

def process_contact_info(contact_block):
    """Извлечение данных из блока контактов."""
    doc = nlp(contact_block)
    phone = None
    email = None

    for ent in doc.ents:
        if ent.label_ == "PHONE":
            phone = ent.text
        elif ent.label_ == "EMAIL":
            email = ent.text

    # Если spaCy не распознал, используем регулярные выражения
    if not phone:
        phone_match = re.search(r"\+?\d[\d\s()-]{7,15}", contact_block)
        phone = phone_match.group(0) if phone_match else None

    if not email:
        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", contact_block)
        email = email_match.group(0) if email_match else None

    return {"phone": phone, "email": email}


import re

def process_personal_info(personal_block):
    """
    Извлечение данных из блока личной информации.
    Комбинирует NER, регулярные выражения и анализ ключевых слов.
    """
    doc = nlp(personal_block)
    data = {}

    # 1. Распознавание имени и фамилии через NER
    name_parts = []
    for ent in doc.ents:
        if ent.label_ == "PER":  # PER - обозначение персоны (имя, фамилия)
            name_parts.append(ent.text.strip())

    # 2. Поиск имени и фамилии через регулярные выражения
    name_regex = r"(?:[A-ZА-Я][a-zа-я]+)\s+(?:[A-ZА-Я][a-zа-я]+)"
    regex_matches = re.findall(name_regex, personal_block)
    if regex_matches:
        name_parts.extend(regex_matches)

    # 3. Поиск имени и фамилии через ключевые слова
    key_phrases = ["имя", "фамилия", "фио", "name", "surname"]
    for phrase in key_phrases:
        match = re.search(rf"(?i){phrase}[:\s]*([A-ZА-Я][a-zа-я]+\s+[A-ZА-Я][a-zа-я]+)", personal_block)
        if match:
            name_parts.append(match.group(1).strip())

    # 4. Убираем дубликаты и объединяем найденные части имени
    unique_name_parts = list(set(name_parts))  # Убираем дубликаты
    if unique_name_parts:
        data["name"] = " ".join(unique_name_parts[:2])  # Берем первые две части (имя и фамилию)

    return data


def process_education(education_block):
    """Извлечение данных из блока образования."""
    doc = nlp(education_block)
    data = {
        "university": None,
        "specialization": None
    }

    for sent in doc.sents:
        if "университет" in sent.text.lower():
            data["university"] = sent.text.split(":")[-1].strip()
        elif "специальность" in sent.text.lower():
            data["specialization"] = sent.text.split(":")[-1].strip()

    return data


# def process_skills(skills_block):
#     """Извлечение навыков."""
#     doc = nlp(skills_block)
#     skills = []
#
#     for line in doc.sents:
#         if any(keyword in line.text.lower() for keyword in ["python", "sql", "machine learning", "aws"]):
#             skills.append(line.text.strip())
#
#     return skills


from typing import List

# Список популярных навыков
SKILLS_KEYWORDS = [
    "python", "sql", "machine learning", "aws", "pandas", "numpy",
    "tensorflow", "keras", "scikit-learn", "docker", "kubernetes",
    "git", "javascript", "html", "css", "react", "node.js", "mongodb",
    "postgresql", "mysql", "data analysis", "data visualization",
    "matlab", "excel", "power bi", "tableau", "api", "rest", "graphql"
]

def process_skills(skills_block: str) -> List[str]:
    """
    Извлечение навыков из текста.
    :param skills_block: Текст блока с навыками.
    :return: Список найденных навыков.
    """
    doc = nlp(skills_block)
    skills = set()  # Используем set для избежания дубликатов

    # Поиск навыков через ключевые слова
    for keyword in SKILLS_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", skills_block.lower()):
            skills.add(keyword)

    # Дополнительный поиск через spaCy (например, именованные сущности)
    for ent in doc.ents:
        if ent.label_ == "TECH" or ent.label_ == "SKILL":  # Если есть кастомные метки для навыков
            skills.add(ent.text.strip().lower())

    return list(skills)
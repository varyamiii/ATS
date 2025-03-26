from PyPDF2 import PdfReader
import json
import re
from typing import Dict
import spacy
from typing import List
from sentence_transformers import SentenceTransformer
#-----------------------------Вспомогательные функции для работы с PDF.
# Загрузка модели spaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

# Инициализация модели SentenceTransformer
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

#Очистка текста: удаляет лишние символы и приводит к нижнему регистру
def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)  # Удаляем знаки препинания
    text = text.lower()  # Приводим к нижнему регистру
    return text

#Токенизация текста (на слова)
def tokenize_text(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    return tokens

#Лемматизация текста: приводит слова к базовой форме
def lemmatize_text(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    return lemmas

#Извлечение сущностей (NER) (компании, даты)
def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

#Создание векторного представления текста
def create_vector(text):
    vector = embedding_model.encode(text)
    return vector
#--------------------------------------------------------------------
from typing import List

SKILLS_KEYWORDS = [
"sql", "java", "api", "python", "javascript", "html", "css", "react", "angular", "vue.js", "postgresql", "mysql", "mongodb", "машинное обучение", "глубокое обучение", "pandas", "numpy", "matplotlib", "hadoop", "spark", "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", "gitlab ci", "git", "devops", "unit testing", "selenium", "rest", "graphql", "linux", "микросервисы", "tensorflow", "pytorch", "алгоритмы", "структуры данных", "nosql", "apache airflow", "talend", "flutter", "swift", "kotlin", "c++", "c#", ".net", "php", "ruby", "bash", "powershell", "terraform", "ansible", "prometheus", "grafana", "kafka", "rabbitmq", "opencv", "computer vision", "natural language processing", "blockchain", "solidity", "rust", "go", "firebase", "elasticsearch", "kibana", "java", "python", "ruby", "php", "node.js", "c#", "go", "rust", "scala", "elixir", "spring", "django", "flask", "express.js", "ruby on rails", "asp.net core", "laravel", "oracle", "mariadb", "sqlite", "redis", "cassandra", "couchbase", "neo4j", "arangodb", "memcached", "varnish", "hazelcast", "rabbitmq", "apache kafka", "activemq", "zeromq", "nats", "event-driven architecture", "cqrs", "ddd", "hexagonal architecture", "grpc", "soap", "openapi", "swagger", "fastapi", "svelte", "ember.js", "backbone.js", "next.js", "nuxt.js", "gatsby", "tailwind css", "bootstrap", "foundation", "bulma", "materialize", "sass", "scss", "less", "stylus", "webpack", "vite", "rollup", "parcel", "babel", "d3.js", "three.js", "chart.js", "pixijs", "redux", "vuex", "zustand", "mobx", "recoil", "jest", "mocha", "chai", "cypress", "playwright", "storybook", "meteor.js", "nestjs", "adonisjs", "fastify", "yeoman", "hygen", "sentry", "logrocket", "datadog", "podman", "lxc", "lxd", "buildah", "nomad", "rancher", "circleci", "travis ci", "bitbucket pipelines", "spinnaker", "pulumi", "cloudformation", "cdk", "crossplane", "elk stack", "loki", "splunk", "new relic", "istio", "envoy", "traefik", "haproxy", "vault", "keycloak", "open policy agent", "scikit-learn", "xgboost", "lightgbm", "catboost", "statsmodels", "jax", "mxnet", "hugging face transformers", "fastai", "nltk", "spacy", "gensim", "textblob", "pil", "pillow", "albumentations", "detectron2", "flink", "hive", "impala", "presto", "drill", "seaborn", "plotly", "bokeh", "altair", "dash", "mlflow", "kubeflow", "tfx", "metaflow", "jetpack compose", "room", "retrofit", "dagger", "hilt", "swiftui", "combine", "coredata", "alamofire", "react native", "xamarin", "ionic", "capacitor", "appium", "espresso", "xctest", "unity", "unreal engine", "godot", "cryengine", "lumberyard", "c++", "c#", "lua", "gdscript", "physx", "bullet physics", "opengl", "directx", "vulkan", "photon", "mirror", "nakama", "blender", "maya", "3ds max", "houdini", "ethereum", "solana", "polkadot", "cardano", "avalanche", "polygon", "vyper", "clarity", "move", "truffle", "hardhat", "brownie", "foundry", "libsodium", "openssl", "bouncy castle", "uniswap sdk", "aave protocol", "compound finance", "erc-721", "erc-1155", "ipfs", "pinata", "burp suite", "owasp zap", "nikto", "nessus", "metasploit", "nmap", "wireshark", "hydra", "owasp dependency-check", "sonarqube", "qradar", "arcsight", "sentinelone", "thehive", "cortex", "misp", "lambda", "s3", "ec2", "rds", "dynamodb", "cloudfront", "ecs", "eks", "azure functions", "blob storage", "aks", "cosmos db", "logic apps", "cloud functions", "bigquery", "pub/sub", "kubernetes engine", "serverless framework", "aws sam", "google cloud run", "aws migration hub", "azure migrate", "google transfer appliance", "c", "assembly", "micropython", "lua", "freertos", "zephyr", "vxworks", "arduino", "raspberry pi", "esp32", "stm32", "mqtt", "coap", "zigbee", "lorawan", "modbus", "keil", "iar embedded workbench", "platformio", "testng", "cucumber", "gauge", "karate", "jmeter", "gatling", "locust", "owasp dependency-check", "snyk", "fortify", "detox", "earlgrey", "xctest", "bdd", "tdd"
]

# Извлечение ключевых навыков из текста
def extract_key_skills(text: str) -> List[str]:
    # Очистка текста
    cleaned_text = clean_text(text)

    # Поиск навыков через ключевые слова
    skills = set()
    for keyword in SKILLS_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", cleaned_text):
            skills.add(keyword)

    # Дополнительный поиск через NER
    entities = extract_entities(cleaned_text)
    for entity, label in entities:
        if label in {"TECH", "SKILL"}:  # Если есть кастомные метки для навыков
            skills.add(entity.lower())

    return list(skills)
#----------------------------------------------------------------------
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


def process_education(education_block: str) -> Dict[str, str]:
    """
    Извлечение данных об образовании и специальности.
    """
    doc = nlp(education_block)
    data = {
        "university": None,
        "specialization": None
    }

    # Списки синонимов для поиска
    university_keywords = ["университет", "институт", "академия", "колледж", "школа", "вузы"]
    specialization_keywords = ["специальность", "профиль", "направление", "квалификация", "дисциплина"]

    # Поиск университета
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in university_keywords):
            # Используем регулярное выражение для извлечения названия
            match = re.search(rf"(?:{'|'.join(university_keywords)}):\s*([^\n]+)", sent.text.lower())
            if match:
                data["university"] = match.group(1).strip()
            else:
                # Если нет явного разделителя, берем всё предложение
                data["university"] = sent.text.strip()

    # Поиск специальности
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in specialization_keywords):
            # Используем регулярное выражение для извлечения специальности
            match = re.search(rf"(?:{'|'.join(specialization_keywords)}):\s*([^\n]+)", sent.text.lower())
            if match:
                data["specialization"] = match.group(1).strip()
            else:
                # Если нет явного разделителя, берем всё предложение
                data["specialization"] = sent.text.strip()

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


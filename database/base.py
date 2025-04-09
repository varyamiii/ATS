# from sqlalchemy import create_engine, Integer, String, ARRAY, Text
# from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
# from typing import List, Optional
#
# # Конфигурация подключения к PostgreSQL
# DATABASE_URL = "postgresql://postgres:sqlritach@localhost:5432/candidate_selection"
#
# # Создание синхронного движка
# engine = create_engine(DATABASE_URL, echo=True)
#
# # Создание сессии
# SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
#
# # Базовый класс для моделей
# class Base(DeclarativeBase):
#     pass
#
# # Модель Candidate
# class Candidate(Base):
#     __tablename__ = "candidates"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     employment_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     work_format: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     education: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     skills: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)
#     experience_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
#     english_level: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     special_requirements: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     resume_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#
# # Модель Criteria
# class Criteria(Base):
#     __tablename__ = "criteria"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     position: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Должность
#     grade: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # Уровень (например, Junior, Middle, Senior)
#     employment_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Тип занятости
#     experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Опыт работы (в годах)
#     education: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Образование
#     skills: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True)  # Массив навыков
#     english_level: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # Уровень английского языка
#     special_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Особые требования
#
# # Функция для создания таблиц
# def init_db():
#     try:
#         Base.metadata.create_all(bind=engine)
#         print("Таблицы успешно созданы.")
#     except Exception as e:
#         print(f"Ошибка при инициализации базы данных: {e}")
#
# # Функция для получения синхронной сессии (Dependency для FastAPI)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# app/config.py
from sentence_transformers import SentenceTransformer

# Инициализация модели
model = SentenceTransformer('all-MiniLM-L6-v2')
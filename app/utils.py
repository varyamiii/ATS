from PyPDF2 import PdfReader
#-----------------------------Вспомогательные функции для работы с PDF.
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Если текст не найден, добавляем пустую строку
    return text
FROM python:3.11-slim

WORKDIR /app

# Копируем из явного контекста
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
COPY tests/ .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
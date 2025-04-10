FROM python:3.11-slim

WORKDIR /app

# Сначала копируем только requirements.txt
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем остальные файлы
COPY src/ src/
COPY tests/ tests/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.11-slim

WORKDIR /app

# Используем абсолютный путь
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/
COPY tests/ /app/tests/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
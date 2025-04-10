FROM python:3.11-slim

WORKDIR /app

# Вместо requirements.txt
RUN pip install --no-cache-dir \
    fastapi==0.68.0 \
    uvicorn==0.15.0 \
    pytest==7.4.0 \
    httpx==0.24.0

COPY src/ src/
COPY tests/ tests/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
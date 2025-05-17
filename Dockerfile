FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--workers", "6", "--bind", "0.0.0.0:8000"]

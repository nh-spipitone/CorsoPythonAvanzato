FROM python:3.12-slim

RUN useradd -m appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y netcat-openbsd

RUN apt-get install -y wget && \
    wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /usr/bin/wait-for-it.sh && \
    chmod +x /usr/bin/wait-for-it.sh && \
    apt-get purge -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
COPY tests/test_api.py /app/tests/test_api.py

ENV FLASK_ENV=production

EXPOSE 8000

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

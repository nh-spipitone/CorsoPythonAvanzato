FROM python:3.12-slim

RUN useradd -m appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
COPY run_simple_checks.py /app/run_simple_checks.py
RUN pip install requests

ENV FLASK_ENV=production

EXPOSE 8000

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libzbar0 \
    libzbar-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "QR_reader_project.wsgi:application", "--bind", "0.0.0.0:8000"]
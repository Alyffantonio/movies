FROM python:3.12-slim

WORKDIR /code


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    unzip \
    libpq-dev \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /code/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

ENV DJANGO_SETTINGS_MODULE=movie_project.settings

EXPOSE 8000

CMD ["gunicorn", "movie_project.wsgi:application", "--bind", "0.0.0.0:8000"]

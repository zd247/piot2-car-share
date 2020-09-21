FROM python:3.7

RUN pip install Flask gunicorn

COPY app/ app/
WORKDIR /app

ENV PORT 5000

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
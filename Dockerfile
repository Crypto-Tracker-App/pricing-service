FROM python:3.14.1-alpine3.23

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV FLASK_APP=wsgi.py
EXPOSE 12000

CMD ["gunicorn", "--bind", "0.0.0.0:12000", "wsgi:app"]

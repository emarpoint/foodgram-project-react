FROM python:3.7-slim

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]



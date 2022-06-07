FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]



# FROM python:3.7-slim

# COPY ./ /app

# WORKDIR /app

# COPY backend/requirements.txt pwd

# RUN pip3 install --upgrade pip && pip3 install -r /app/backend/requirements.txt --no-cache-dir

# CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]

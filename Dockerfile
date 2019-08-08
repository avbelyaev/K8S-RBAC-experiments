FROM python:alpine3.6

COPY requirements.txt /app
WORKDIR /app

RUN apk update
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]

FROM python:3-alpine

RUN apk update

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]

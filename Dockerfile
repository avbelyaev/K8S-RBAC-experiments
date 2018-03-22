FROM python:3-alpine

COPY . /app

WORKDIR /app

RUN apk update
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]

FROM python:alpine3.8

WORKDIR /app
COPY requirements.txt /app

RUN apk update
RUN pip install -r requirements.txt --no-cache-dir

COPY app.py /app

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]

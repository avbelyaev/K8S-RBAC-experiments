FROM python:alpine3.7

WORKDIR /app
COPY requirements.txt /app

RUN apk update
RUN pip install -r requirements.txt --no-cache-dir

COPY backend /app/backend
COPY main.py /app

EXPOSE 5000

ENTRYPOINT ["python", "main.py"]

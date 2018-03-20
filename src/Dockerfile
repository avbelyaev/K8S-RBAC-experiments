FROM python:3-alpine

COPY . /flask-app

WORKDIR /flask-app

RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

EXPOSE 5000

ENTRYPOINT ["python", "app/app.py"]

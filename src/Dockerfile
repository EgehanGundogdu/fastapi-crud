FROM python:3.9-alpine

WORKDIR /usr/src/app


RUN apk add build-base && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    libc-dev linux-headers postgresql-dev zlib zlib-dev python3-dev \
    && apk add --update musl-dev gcc libffi-dev

COPY . /usr/src/app/


RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apk del .tmp-build-deps
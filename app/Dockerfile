FROM python:3.7.0-alpine
WORKDIR /usr/src/app

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev libressl-dev python3-dev

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /user/src/app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
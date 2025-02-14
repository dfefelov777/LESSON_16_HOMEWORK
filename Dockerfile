FROM python:3.10-slim

RUN rm -rf staticfiles/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ../../Downloads/Otus_Professional_Python_Homework_08-main .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#RUN python manage.py collectstatic --noinput
#RUN python manage.py migrate --noinput

# ЗАПРОСИТЬ СТИЛИ в СТАТИК и дальше по ДЗ....

ENTRYPOINT ["/entrypoint.sh"]
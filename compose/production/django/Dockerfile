FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi

# Requirements are installed here to ensure they will be cached.
COPY ./app/requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/production/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/production/django/celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r//' /start-flower.sh
RUN chmod +x /start-flower.sh

COPY ./app /app

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]

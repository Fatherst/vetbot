FROM python:3.10

RUN apt-get update && apt-get install -y nginx

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE 'bot_admin.settings'

RUN apt-get update \
    && apt-get install -y netcat-traditional \
    && apt-get install -y gettext

COPY requirements.txt requirements.txt
COPY run_asgi.sh run_asgi.sh

RUN mkdir -p /opt/app/static/ \
    && mkdir -p /opt/app/media/ \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN sed -i 's/\r$//g' /opt/app/run_asgi.sh \
    && chmod +x  /opt/app/run_asgi.sh

# Копирование конфигурационных файлов Nginx
COPY .scratch /
RUN System_type="$(dpkg --print-architecture | sed "s/amd64/x86_64/")" \
    && wget -q -O- https://github.com/just-containers/s6-overlay/releases/download/v3.1.0.1/s6-overlay-noarch.tar.xz | tar -C / -Jxp \
    && wget -q -O- https://github.com/just-containers/s6-overlay/releases/download/v3.1.0.1/s6-overlay-$System_type.tar.xz | tar -C / -Jxp \
    && rm -rf .scratch;
    
EXPOSE 8000

ENTRYPOINT ["/init"]
# python 3.10.8버전 이미지를 사용해 빌드
FROM python:3.10.8



# FROM alexshin/docker-django-asgi-daphne

# ENV DAPHNE_PORT=8000
# ENV APP_ASGI_ENTRYPOINT=handsup.asgi:channel_layer
# ENV DJANGO_SETTINGS_MODULE=handsup.settings

# COPY . ${APP_WORKDIR}

# This is only needed if daphne is going to be running behind a proxy like nginx.
# CMD ["--proxy-headers"]

# .pyc 파일을 생성하지 않도록 설정합니다.
ENV PYTHONDONTWRITEBYTECODE 1

# 파이썬 로그가 버퍼링 없이 즉각적으로 출력하도록 설정합니다.
ENV PYTHONUNBUFFERED 1

# /app/ 디렉토리를 생성합니다.
RUN mkdir /app/

# /app/ 경로를 작업 디렉토리로 설정합니다.
WORKDIR /app/

# crontab 설치
RUN apt-get update -y
RUN apt-get install -y cron

# requirments.txt를 작업 디렉토리(/app/) 경로로 복사합니다.
COPY ./requirements.txt .

# 프로젝트 실행에 필요한 패키지들을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# CMD service cron start
# CMD python manage.py crontab add

# gunicorn과 postgresql을 사용하기 위한 패키지를 설치합니다.
RUN pip install gunicorn psycopg2


# Python 3.11.9 이미지를 사용합니다.
FROM python:3.11.9-slim

# 작업 디렉터리를 설정합니다.
WORKDIR /app

# 필요한 시스템 패키지를 설치합니다.
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 필요한 Python 패키지를 설치합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드를 복사합니다.
COPY . .

# gunicorn을 사용하여 Django 앱 실행
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "musicgenerator.wsgi:application"]
# Stage 1: Build with Poetry
FROM python:3.11.11-slim AS builder

ENV POETRY_VERSION=2.1.3
WORKDIR /opt

# 빌드에 필요한 패키지 추가 설치
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
COPY poetry-2.1.3-py3-none-any.whl .
RUN pip install ./poetry-2.1.3-py3-none-any.whl && \
    poetry --version

# 프로젝트 복사 및 의존성 설치
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry install --no-root

# Stage 2: Runtime 이미지 (최종 배포용)
FROM python:3.11.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/tmp/poetry'

WORKDIR /app

# 런타임에도 필요한 패키지 설치 (C 확장 의존성)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 실행에 필요한 파이썬 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# 앱 복사
COPY . /app

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

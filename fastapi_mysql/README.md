# FastAPI BoilerPlate

## 1. 구성

- Framework: fastapi
- Database: mysql
- Log Database: mongo
- Architecture: clean architecture

## 2. 기동

### 1. Infra

### 2. Application

## 3. 테스트

### 1. 전체 테스트 수행

```
pytest src/tests/
```

## 4. env

```
##############################
# JWT
##############################
JWT_ALGORITHM=HS256
JWT_SECRET_KEY=Y2hhdGNsLXNlY3JldC0xMiMkNTYmKg==
ACCESS_TOKEN_EXPIRES_IN=99999
REFRESH_TOKEN_EXPIRES_IN=1


##############################
# MYSQL
##############################
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_ID=admin
MYSQL_PW=admin1234!
MYSQL_DB=python_fastapi

##############################
# RabbitMQ
##############################
RABBITMQ_HOST=127.0.0.1
RABBITMQ_ID=admin
RABBITMQ_PW=admin1234!


##############################
# MongoDB SETTINGS
# 5초 동안 응답이 없으면 연결 실패
# 5초 동안 응답이 없으면 소켓 연결 종료
# 5초 동안 서버 선택 실패 시 예외 발생
##############################
MONGODB_CONN_SERV=mongodb+srv://
# 로컬
MONGODB_HOST=localhost
# # 컨테이너
# MONGODB_HOST=mongo
MONGODB_PORT=27017
MONGODB_DB=python_fastapi
MONGODB_ID=admin
MONGODB_PW=admin1234!
MONGODB_LOG_COL=log
CONNECTION_TIMEOUT_MS=5000
SOCKET_TIMEOUT_MS=5000
SERVER_SELECTION_TIMEOUT_MS=5000
RELOAD_PERIOD=3600
QUERY_STRING=authSource=admin&directConnection=true&retryWrites=true&w=majority
# 개발/운영
# QUERY_STRING=authSource=admin&replicaSet=rs0&retryWrites=true&w=majority
```

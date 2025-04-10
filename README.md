# DobrynyaNN Mock API

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com)
[![Uvicorn](https://img.shields.io/badge/Server-Uvicorn-ff69b4)](https://www.uvicorn.org)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue)](https://www.docker.com/)

Mock API сервис для тестирования и разработки приложения **DobrynyaNN**

## 📦 Требования
- [Docker](https://www.docker.com/) установлен и запущен
- [Docker Compose](https://docs.docker.com/compose/) (обычно уже входит в Docker Desktop)


## 🔧 Установка и запуск

### 1. Клонируйте репозиторий:

```bash
git clone https://github.com/tniur/dobrynya-mock-api.git
cd dobrynya-mock-api
```

## 2. Запустите сервер:
```bash
docker-compose up --build
```

## 3. Сервер доступен по адресу:
- http://127.0.0.1:8000

### 📚 Документация API
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 4. Остановить сервер:
```bash
docker-compose down
```
# Dobrynya Mock API

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com)
[![Uvicorn](https://img.shields.io/badge/Server-Uvicorn-ff69b4)](https://www.uvicorn.org)

Mock API сервис для тестирования и разработки приложения DobrynyaNN

## ⚙️ Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/tniur/dobrynya-mock-api.git
cd dobrynya-mock-api
```
### 2. Создайте и активируйте виртуальное окружение

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установите зависимости
```bash
pip install -r app/requirements.txt
```

## 🚀 Запуск сервера
```bash
uvicorn app.main:app --reload
```

Cервер будет доступен по адресу: http://127.0.0.1:8000

## 📚 Документация API
- Swagger UI: /docs
- ReDoc: /redoc

## ⚠️ Требования
- Python 3.8+
- pip 20+
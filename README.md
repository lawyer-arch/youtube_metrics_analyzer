# youtube_metrics_analyzer
Приложение читает файлы с данными о видео (см. пример ниже) и формирует отчеты

## Установка и запуск


### 1. Клонирование репозитория

```
git clone <repository-url>
```
```
cd youtube_metrics_analyzer
```

### 2. Создание виртуального окружения
```
python -m venv venv
```
```
source venv/bin/activate  # Linux/Mac
```
или
```
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```
pip install -e ".[dev]"
```

### 4. Запуск
```
python3 main.py --files tests/fixtures/valid_data.csv tests/fixtures/empty_data.csv --report clickbait
```

### 5. Для разработки (с тестами)
```
pip install pytest pytest-cov black isort mypy
```
```
pytest
```


# Использование

### Базовый запуск

```
python main.py --files stats1.csv --report clickbait
```

### Анализ нескольких файлов

```
python main.py --files stats1.csv stats2.csv --report clickbait
```

### После установки пакета можно использовать команду

```
youtube-analyzer --files stats1.csv --report clickbait
```


# Тестирование

### Установка зависимостей для разработки
```
pip install -e ".[dev]"
```

### Запуск тестов
```
python -m pytest -v
```

### Запуск с покрытием
```
pytest --cov=src --cov-report=html
```

### Запуск только интеграционных тестов
```
pytest tests/test_integration.py -v
```

### Запуск с подробным выводом
```
pytest -v --tb=short
```

### Запуск с покрытием
```
pytest --cov=src --cov-report=term-missing
```

## Форматирование кода
```
black src tests
isort src tests
```

## Проверка типов
```
mypy src
```
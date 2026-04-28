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
pip install tabulate
```

### 4. Запуск
```
python main.py --files stats1.csv --report clickbait
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
pytest
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
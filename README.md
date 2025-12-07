# Мини-система сбора и анализа данных

Цель: создать простую end-to-end систему, которая генерирует данные, сохраняет их и позволяет анализировать через Redash и Jupyter Notebook.

## Компоненты системы

1. ### Генератор данных (Python)
   - Создаёт записи каждые 5 секунд
   - Реалистичные значения для фитнес-трекера: шаги, пульс, калории, тип активности
   - Поддержка **10 пользователей** с устойчивым поведением
   - Автоматически запускается при старте Docker

2. ### База данных: PostgreSQL
   - Хранит все события в таблице `fitness_data`
   - Структура:
     ```sql
     id SERIAL PRIMARY KEY,
     timestamp TIMESTAMP DEFAULT NOW(),
     user_id INTEGER,
     steps INTEGER,
     heart_rate INTEGER,
     calories DECIMAL(5,2),
     activity_type VARCHAR(50)
     ```

3. ### Визуализации: Redash
   - Дашборд: `Fitness Analytics Dashboard`
   - Источник данных: PostgreSQL (`analytics_db`)
   - Доступен по адресу: [http://localhost:5000](http://localhost:5000)

4. ### Анализ: Jupyter Notebook
   - Файл: `notebooks/analysis.ipynb`
   - Проводит исследовательский анализ с использованием `pandas` и `matplotlib`
   - Строит графики по пользователям и активностям

## Как запустить

1. Убедитесь, что установлены:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Git

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-ник/mini-data-system.git
   cd mini-data-system

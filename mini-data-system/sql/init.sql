-- Создаём таблицу для данных фитнес-трекера
CREATE TABLE IF NOT EXISTS fitness_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    steps INTEGER NOT NULL,
    heart_rate INTEGER NOT NULL,
    calories DECIMAL(5,2) NOT NULL,
    activity_type VARCHAR(50) NOT NULL
);
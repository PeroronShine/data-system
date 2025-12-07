import time
import random
import psycopg2
from datetime import datetime

# Функция подключения к базе данных
def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",  # имя сервиса из docker-compose.yml
                database="analytics_db",
                user="user",
                password="pass"
            )
            print("✅ Успешно подключено к базе данных")
            return conn
        except psycopg2.OperationalError as e:
            print("❌ Не могу подключиться к БД, жду 2 сек... Ошибка:", e)
            time.sleep(2)

def generate_fitness_data():
    activity = random.choices(
        ['walking', 'running', 'resting'],
        weights=[0.5, 0.3, 0.2]
    )[0]

    if activity == 'walking':
        steps = random.randint(50, 150)
        heart_rate = random.randint(80, 120)
        calories = round(steps * 0.08 + (heart_rate - 70) * 0.05, 2)
    elif activity == 'running':
        steps = random.randint(150, 300)
        heart_rate = random.randint(120, 180)
        calories = round(steps * 0.12 + (heart_rate - 70) * 0.07, 2)
    else:  # resting
        steps = random.randint(0, 10)
        heart_rate = random.randint(60, 80)
        calories = round(steps * 0.05 + (heart_rate - 70) * 0.03, 2)

    return steps, heart_rate, calories, activity

def main():
    print("Запуск генератора данных...")
    conn = connect_to_db()
    cursor = conn.cursor()

    print("Генератор начал работу. Данные будут добавляться каждую секунду.\n")

    try:
        while True:
            steps, heart_rate, calories, activity = generate_fitness_data()

            # Вставляем в таблицу
            cursor.execute(
                """
                INSERT INTO fitness_data (steps, heart_rate, calories, activity_type)
                VALUES (%s, %s, %s, %s)
                """,
                (steps, heart_rate, calories, activity)
            )
            conn.commit()

            # Лог в консоль
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Добавлено: {steps} шагов, пульс={heart_rate}, "
                  f"калории={calories:.2f}, активность='{activity}'")

            time.sleep(2) 

    except KeyboardInterrupt:
        print("\nГенератор остановлен пользователем.")
    except Exception as e:
        print("❗ Ошибка:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
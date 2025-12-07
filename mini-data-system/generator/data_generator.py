import time
import random
import psycopg2
from datetime import datetime

USER_IDS = list(range(1, 11))  

user_states = {
    user_id: {
        "activity": random.choice(['walking', 'running', 'resting']),
        "duration": 0
    } for user_id in USER_IDS
}

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",
                database="analytics_db",
                user="user",
                password="pass"
            )
            print("✅ Успешно подключено к базе данных")
            return conn
        except psycopg2.OperationalError as e:
            print("❌ Не могу подключиться к БД, жду 2 сек... Ошибка:", e)
            time.sleep(2)

def generate_activity(user_state):
    current_activity = user_state["activity"]
    duration = user_state["duration"]

    # С вероятностью 3% меняем активность после минимум 10 секунд
    if duration > 10 and random.random() < 0.03:
        current_activity = random.choices(
            ['walking', 'running', 'resting'],
            weights=[0.5, 0.3, 0.2]
        )[0]
        user_state["activity"] = current_activity
        user_state["duration"] = 0

    user_state["duration"] += 1

    if current_activity == 'walking':
        steps = random.randint(1, 3)  # 60–180 шагов/мин
        heart_rate = random.randint(80, 120)
        calories = round(steps * 0.08 + (heart_rate - 70) * 0.05, 2)
    elif current_activity == 'running':
        steps = random.randint(4, 6)  # 240–360 шагов/мин
        heart_rate = random.randint(140, 180)
        calories = round(steps * 0.12 + (heart_rate - 70) * 0.07, 2)
    else:  # resting
        steps = 0
        heart_rate = random.randint(60, 80)
        calories = round(0.1, 2)

    return steps, heart_rate, calories, current_activity

def main():
    print("🔄 Запуск генератора данных...")
    conn = connect_to_db()
    cursor = conn.cursor()

    print("🟢 Генератор начал работу. Данные будут добавляться каждые 5 секунд.\n")

    try:
        while True:
            # Каждые 5 секунд обновляем данные для всех пользователей
            for user_id in USER_IDS:
                state = user_states[user_id]
                steps, heart_rate, calories, activity = generate_activity(state)

                # Вставляем в таблицу
                cursor.execute(
                    """
                    INSERT INTO fitness_data (user_id, steps, heart_rate, calories, activity_type)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, steps, heart_rate, calories, activity)
                )

            conn.commit()

            # Лог в консоль
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Добавлено {len(USER_IDS)} записей (по одной на пользователя)")

            # Ждём 5 секунд — как реальный интервал синхронизации трекера
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Генератор остановлен пользователем.")
    except Exception as e:
        print("❗ Ошибка:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

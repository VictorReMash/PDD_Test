import mysql.connector

# Настройки подключения к базе данных
db_config = {
    "user": "usertest",
    "password": "4MDI8c81",
    "host": "localhost",
    "database": "test_form",
}
# Подключаемся к базе данных
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Выполняем запрос к базе данных
query = "SELECT id, name FROM chapters where id = 2"
cursor.execute(query)

# Получаем все строки результата
rows = cursor.fetchall()

# Выводим данные
for row in rows:
    print(*row)

# Закрываем курсор и соединение
cursor.close()
conn.close()

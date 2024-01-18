import psycopg2

# Замените значения на свои
host = "127.0.0.1"
port = "5432"
user = "anyavoitovich"
password = ""
database = "marketplace"

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    print("Connected to the database")

    # Создайте объект курсора
    cursor = connection.cursor()

    # Создание таблицы пользователей
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        role VARCHAR(20) NOT NULL
    );
    '''
    cursor.execute(create_table_query)

    # Сохранение изменений
    connection.commit()
    print("Table 'users' created successfully")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL or creating table:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Connection to PostgreSQL closed")


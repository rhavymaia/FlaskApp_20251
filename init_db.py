import psycopg2

# 1 - Abri a conexão
connection = psycopg2.connect(user="postgres",
                              password="123456",
                              host="127.0.0.1",
                              port="5434",
                              database="censoescolar")
cursor = connection.cursor()

# 2 - Cursor
# 3 - Executar
with open('schemas.sql') as f:
    cursor.execute(f.read())

# 4 - Commit ou fecth
connection.commit()

# 5 - Fechar
connection.close()

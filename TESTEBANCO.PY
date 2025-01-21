import psycopg2

try:
    connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="GGSjun2024",
        host="database-1.cb6awmsm2t69.us-east-1.rds.amazonaws.com",
        port="5432",
    )
    print("Conexão bem-sucedida!")
    connection.close()
except Exception as e:
    print("Erro ao conectar ao banco:", e)

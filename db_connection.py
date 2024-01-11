import psycopg2
from config import HOST, USER, PASSWORD, DB_NAME, PORT

def connect_to_db():
    try:
        CONNECTION = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME,
            port=PORT
        )
        CONNECTION.autocommit = True
        print("[INFO] Successfully connected to database")

        with CONNECTION.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS schedules(
                    id int NOT NULL UNIQUE,
                    sport_type_name varchar(20),
                    tournament_name varchar(50),
                    date_time varchar(20),
                    first_team_name varchar(20),
                    second_team_name varchar(20));"""
            )
        return CONNECTION
    except:
        print('Something wrong with DB Conncetion, check the params of connection!')
        return None
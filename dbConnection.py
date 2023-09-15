import psycopg2
from config import HOST, USER, PASSWORD, DB_NAME, PORT


def connect_to_db():
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


def get_db_data(CONNECTION):
    with CONNECTION.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM schedules;"""
        )
        print(cursor.fetchall())


def add_item(CONNECTION, item):
    with CONNECTION.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO schedules(id, sport_type_name, tournament_name, date_time, first_team_name, second_team_name)
                VALUES ({item['id']},'{item['sport']}', '{item['token']}', '{item['date_time']}', '{item['team1']}', '{item['team2']}')
                ON CONFLICT(id) DO NOTHING;
            """
        )

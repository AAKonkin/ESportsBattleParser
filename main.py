import psycopg2
import time
import aiohttp
import asyncio
import datetime
from config import HOST, USER, PASSWORD, DB_NAME, PORT, DURATION_TIME
MONTH = str(datetime.date.today().month) if (
    datetime.date.today().month >= 10) else "0"+str(datetime.date.today().month)
NEXT_MONTH = str(int(MONTH)+1) if (int(MONTH)+1 >=
                                   10) else "0"+str(int(MONTH)+1)
# https://curlconverter.com


async def get_cs_go_data(CONNECTION):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://csgo.esportsbattle.com/api/tournaments?dateFrom=2023-{MONTH}-01T21%3A00%3A00.000Z&dateTo=2023-{NEXT_MONTH}-01T20%3A59%3A59.000Z&page=1') as response:
            response = await response.json()
            result = list(map(lambda r: [r["id"], r["token"][:len(
                r["token"])-14], r["date"][:10]], list(response["tournaments"])))
    for res in result:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://csgo.esportsbattle.com/api/tournaments/{res[0]}/matchesWithMaps') as response:
                response = await response.json()
                for n in range(2):
                    event = response[n]
                    id = event["id"]
                    date = event["date"][:10]
                    event_time = event["date"][11:16]
                    team1 = event["participant1"]["team"]["token"]
                    team2 = event["participant2"]["team"]["token"]
                    print(date, event_time, team1, team2)
                    with CONNECTION.cursor() as cursor:
                        cursor.execute(
                            f"""INSERT INTO schedules(id, sport_type_name, tournament_name, date_time, first_team_name, second_team_name)
                                VALUES ({id},'CS:GO', '{res[1]}', '{date+" "+event_time}', '{team1}', '{team2}') 
                                ON CONFLICT(id) DO NOTHING;
                            """
                        )


async def get_football_data(CONNECTION):
    events = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://football.esportsbattle.com/api/tournaments?page=1&dateFrom=2023%2F{MONTH}%2F1+05%3A00&dateTo=2023%2F{NEXT_MONTH}%2F1+20%3A59') as response:
            response = await response.json()
            pages = response["totalPages"]
    for page in range(1, pages+1):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://football.esportsbattle.com/api/tournaments?page={page}&dateFrom=2023%2F{MONTH}%2F1+05%3A00&dateTo=2023%2F{NEXT_MONTH}%2F1+20%3A59') as response:
                response = await response.json()
                events.extend(list(map(lambda r: [r["id"], r["token_international"][:len(
                    r["token_international"])-11], r["status_id"]], list(response["tournaments"]))))
    for event in events:
        if event[2] in (2, 3):
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://football.esportsbattle.com/api/tournaments/{event[0]}/matches') as response:
                    response = list(await response.json())
                    result = list(map(lambda r: [r["id"], r["date"][:10], r["date"][11:16], r["status_id"],
                                                 r["participant1"]["nickname"], r["participant2"]["nickname"]], list(response)))
                    for res in result:
                        if res[3] in (1, 2):
                            with CONNECTION.cursor() as cursor:
                                cursor.execute(
                                    f"""INSERT INTO schedules(id, sport_type_name, tournament_name, date_time, first_team_name, second_team_name)
                                        VALUES ({res[0]},'FOOTBALL', '{event[1]}', '{res[1]+" "+res[2]}', '{res[4]}', '{res[5]}')
                                        ON CONFLICT(id) DO NOTHING;
                                    """
                                )


def main():
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

        while True:
            print("Start parsing...")
            asyncio.run(get_cs_go_data(CONNECTION))
            asyncio.run(get_football_data(CONNECTION))
            # -----DEBUGGING-----
            with CONNECTION.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM schedules;"""
                )
                print(cursor.fetchall())
            # -------------------
            print("Waiting for 60 seconds...")
            time.sleep(DURATION_TIME)

    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)
    finally:
        if CONNECTION:
            CONNECTION.close()
            print("[INFO] PostgreSQL connection closed")


if __name__ == "__main__":
    main()

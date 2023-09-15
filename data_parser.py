import datetime
from aiohttp import ClientSession
import asyncio
import requests


async def get_all_data(CONNECTION):
    get_cs_go_data(CONNECTION)
    # get_football_data(CONNECTION)


async def get_cs_go_data(CONNECTION):
    result = []
    async with ClientSession as session:
        tasks = []
        for page in range(1, get_pages()+1):
            tasks.append(asyncio.create_task(get_one_page_data(session, page)))
        result = await asyncio.gather(*tasks)

    # запрос на количество страниц
    # постраничное получение данных по турнирам
    # потурнирное получение данных об матче

# async def get_cs_go_data(CONNECTION):
#     pages_data = get_pages_data(CSGO_URL)
#     for pd in pages_data:
#         print(pd)
    # tournaments = get_tournaments(CSGO_URL, pages_data)
    # for tour in tournaments:
    #     print(tour)


# def get_football_data(CONNECTION):
#     pages = get_pages(FOOTBALL_URL)
#     data = get_pages_data(FOOTBALL_URL, pages)
#     for res in data:
#         print(res)


def get_pages(url):
    return requests.get(url, params=get_params(), headers=headers).json()['totalPages']


def get_pages_data(url) -> list:
    result = []
    for page in range(1, get_pages(url)+1):
        response = asyncio.run(get_one_page_data(
            url, params=get_params(page), headers=headers))
        result.extend(list(
            map(lambda item:
                [
                    item["id"],
                    item["token_international"].split(" 2023")[0],
                    (item["date"] if "date" in item else item["start_date"]).split(
                        'T')[0]
                ], list(response["tournaments"])))
        )
    return result


async def get_one_page_data(session, url, params: dict, headers: dict):
    async with session.get(url, params=params, headers=headers) as response:
        return await response.json()


def get_tournaments(url, pages_data):
    result = []
    for res in pages_data:
        result.append(asyncio.run(
            get_one_tournament_data(url, res[0], 'WithMaps')))


async def get_one_tournament_data(url, id: int, end=''):
    async with ClientSession() as session:
        async with session.get(f'{url}/{id}/matches{end}') as response:
            return await response.json()


def get_matches(tournaments):
    for item in tournaments:
        if item["status_id"] in ('15bfd86e-0b4b-4397-bffa-61c9c82d0b66', 1, 2):
            event = item
            id = event["id"]
            date = event["date"][:10]
            event_time = event["date"][11:16]
            team1 = event["participant1"]["team"]["token"] if "team" in event["participant1"] else event["participant1"]["nickname"]
            team2 = event["participant2"]["team"]["token"] if "team" in event["participant2"] else event["participant2"]["nickname"]
            print(date, event_time, team1, team2)

            # item = {'id': id, 'sport': 'CS:GO',
            #         'token': res[1], 'date_time': date+" "+event_time, 'team1': team1, 'team2': team2}
    # CSGO
    # finished - ac853d2a-18c5-48f7-9fbb-59f56eee101d
    # finished - ac853d2a-18c5-48f7-9fbb-59f56eee101d
    # started - 0e35b4fd-a642-491c-b271-9747002693e9
    # planned - 15bfd86e-0b4b-4397-bffa-61c9c82d0b66
    # planned - 15bfd86e-0b4b-4397-bffa-61c9c82d0b66

    # FOOTBALL
    # finished - 4
    # finished - 4
    # started -
    # started -
    # planned - 1, 2
    # planned - 1, 2

    #     async with session.get(f'https://football.esportsbattle.com/api/tournaments/{event[0]}/matches') as response:
    #          response = list(await response.json())
    #          result = list(map(lambda r: [r["id"], r["date"][:10], r["date"][11:16], r["status_id"],
    #                                              r["participant1"]["nickname"], r["participant2"]["nickname"]], list(response)))

    #    async with session.get(f'https://csgo.esportsbattle.com/api/tournaments/{res[0]}/matchesWithMaps') as response:
    #         response = await response.json()
    #         for n in range(2):
    #             event = response[n]
    #             id = event["id"]
    #             date = event["date"][:10]
    #             event_time = event["date"][11:16]
    #             team1 = event["participant1"]["team"]["token"]
    #             team2 = event["participant2"]["team"]["token"]
    #             print(date, event_time, team1, team2)

    # matches = get_matches(tournaments)
    # item = {'id': id, 'sport': 'CS:GO', 'token': res[1], 'date_time': date+" "+event_time, 'team1': team1, 'team2': team2}

    # async with aiohttp.ClientSession() as session:
    #     async with session.get(f'https://csgo.esportsbattle.com/api/tournaments/{res[0]}/matchesWithMaps') as response:
    #         response = await response.json()
    #         for n in range(2):
    #             event = response[n]
    #             id = event["id"]
    #             date = event["date"][:10]
    #             event_time = event["date"][11:16]
    #             team1 = event["participant1"]["team"]["token"]
    #             team2 = event["participant2"]["team"]["token"]
    #             print(date, event_time, team1, team2)

    # events = []
    # for event in events:
    #     if event[2] in (2, 3):
    #         async with aiohttp.ClientSession() as session:
    #             async with session.get(f'https://football.esportsbattle.com/api/tournaments/{event[0]}/matches') as response:
    #                 response = list(await response.json())
    #                 result = list(map(lambda r: [r["id"], r["date"][:10], r["date"][11:16], r["status_id"],
    #                                              r["participant1"]["nickname"], r["participant2"]["nickname"]], list(response)))
    #                 for res in result:
    #                     if res[3] in (1, 2):
    #                         with CONNECTION.cursor() as cursor:
    #                             cursor.execute(
    #                                 f"""INSERT INTO schedules(id, sport_type_name, tournament_name, date_time, first_team_name, second_team_name)
    #                                     VALUES ({res[0]},'FOOTBALL', '{event[1]}', '{res[1]+" "+res[2]}', '{res[4]}', '{res[5]}')
    #                                     ON CONFLICT(id) DO NOTHING;
    #                                 """
    #                             )


CSGO_URL = 'https://csgo.esportsbattle.com/api/tournaments'
FOOTBALL_URL = 'https://football.esportsbattle.com/api/tournaments'

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,la;q=0.8,cy;q=0.7',
    'content-type': 'application/json',
    'if-none-match': 'W/"287-zvcNI2cCPa624XSmqD9RC580Hgo"',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.704 Yowser/2.5 Safari/537.36',
}

MONTH = str(datetime.date.today().month) if (
    datetime.date.today().month >= 10) else "0" + str(datetime.date.today().month)
NEXT_MONTH = str(
    int(MONTH) + 1) if (int(MONTH) + 1 >= 10) else "0"+str(int(MONTH) + 1)


def get_params(page=1):
    return {
        'dateFrom': f'2023-{MONTH}-01T21:00:00.000Z',
        'dateTo': f'2023-{NEXT_MONTH}-01T20:59:59.000Z',
        'page': page,
    }

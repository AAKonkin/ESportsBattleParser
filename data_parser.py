import aiohttp
from config import CSGO_URL as CS_GO, FOOTBALL_URL as Football, headers, get_params, headers, YEAR

async def get_all_data(CONNECTION):
    all_data = []
    for sport in [CS_GO, Football]:
        print(f"Get data for {sport.title()}")
        all_data.extend(await get_data(sport))
    print("All Data:")
    print(*all_data)

    # SOMETHIND LOGIC FOR DB ACTIONS

async def get_data(url) -> list:
    tournaments = await get_pages_data(url)
    result = []
    if (tournaments):
        result = await get_tournaments_data(url, tournaments)
        print("Already getted")
    else:
        print("No Data")
    return result

async def get_pages_data(url) -> list:
    tournaments = []
    page = 1
    while (True):
        response = await get_one_page_data(url, params=get_params(page), headers=headers)
        if (response['totalPages'] == 0):
            break
        tournaments.extend(list(
            map(lambda item:
                [
                    item["id"],
                    item["token_international"].split(f" {YEAR}")[0],
                    (item["date"] if "date" in item else item["start_date"]).split(
                        'T')[0]
                ], list(response["tournaments"]))))
        page += 1
        if (page == response['totalPages'] + 1): break
    return tournaments

async def get_one_page_data(url, params: dict, headers: dict) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers, ssl=False) as response:
            return await response.json()

async def get_tournaments_data(url, tournaments: list) -> list:
    result = []
    for tournament in tournaments:
        response = await get_one_tournament_data(url, tournament[0])
        for item in response:
            event = item
            id = event["id"]
            date = event["date"][:10]
            event_time = event["date"][11:16]
            team1 = event["participant1"]["team"]["token"] if "team" in event["participant1"] else \
                event["participant1"]["nickname"]
            team2 = event["participant2"]["team"]["token"] if "team" in event["participant2"] else \
                event["participant2"]["nickname"]
            result.append(
                {'id': id, 'sport': 'Football', 'token': tournament[1], 'date_time': date + " " + event_time, 'team1': team1,
                 'team2': team2})
    return result

async def get_one_tournament_data(url, id: int) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url}/{id}/matches', ssl=False) as response:
            return await response.json()

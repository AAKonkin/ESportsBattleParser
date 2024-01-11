import datetime
HOST = "localhost"
USER = "postgres"
PASSWORD = "12345"
DB_NAME = "postgres"
PORT = "5432"
DURATION_TIME = 60
CSGO_URL = 'https://csgo.esportsbattle.com/api/tournaments'
FOOTBALL_URL = 'https://football.esportsbattle.com/api/tournaments'

headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Accept-Language': 'ru',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
}

MONTH = str(datetime.date.today().month) if (
    datetime.date.today().month >= 10) else "0" + str(datetime.date.today().month)
NEXT_MONTH = str(
    int(MONTH) + 1) if (int(MONTH) + 1 >= 10) else "0"+str(int(MONTH) + 1)
YEAR = str(datetime.date.today().year)

def get_params(page=1):
    return {
        'dateFrom': f'{YEAR}-{MONTH}-{datetime.date.today().day}T21:00:00.000Z',
        'dateTo': f'{YEAR}-{NEXT_MONTH}-01T20:59:59.000Z',
        'page': page,
    }

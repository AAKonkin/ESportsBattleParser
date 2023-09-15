from dbConnection import connect_to_db
from data_parser import get_all_data, asyncio
from config import DURATION_TIME


async def set_sleep():
    asyncio.sleep(DURATION_TIME)


async def main():
    CONNECTION = connect_to_db()
    while True:
        print("Start parsing...")
        asyncio.run(get_all_data(CONNECTION))
        print("Waiting for 60 seconds...")
        await set_sleep()

asyncio.run(main())

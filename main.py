from db_connection import connect_to_db
from config import DURATION_TIME
from data_parser import get_all_data
import time
import asyncio

def main():
    CONNECTION = connect_to_db()
    if (CONNECTION):
        print('Start parsing...')
        while(True):
            asyncio.run(get_all_data(CONNECTION))
            print('Waiting for 60 seconds')
            time.sleep(DURATION_TIME)

if __name__ == '__main__':
    main()

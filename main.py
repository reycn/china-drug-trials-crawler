import asyncio
import time

import pandas as pd
from termcolor import cprint

from lib.df import save_df, sort_df
from lib.fetch import get_detail


def generate_ids(start: int = 1247,
                 end: int = 1464,
                 prefix: str = 'CTR2021') -> list:
    '''Generate continuous trial ids'''
    trials = [prefix + str(trial) for trial in range(start, end + 1)]
    return trials


async def run() -> None:
    '''Running the procedure'''
    trials = generate_ids()
    df = pd.DataFrame()
    for i in range(len(trials)):
        cprint(f'Handling: No.{i+1} / {trials[i]}', 'white', 'on_green')
        dictionary = await get_detail(trials[i])
        df = df.append(dictionary, ignore_index=True)
    df = sort_df(df)
    save_df(df)
    # time.sleep(3)


if __name__ == '__main__':
    '''Default function / testing function'''
    trial_id = 'CTR20211247'
    try:
        time_start = time.time()
        cprint('Start running...', 'white', 'on_green')
        asyncio.get_event_loop().run_until_complete(run())
        time_end = time.time()
        cprint(f"Total time: {str(time_end-time_start)[:5]}s.", 'white',
               'on_green')
    except KeyboardInterrupt as k:
        cprint('\nKey pressed to interrupt...', 'white', 'on_red')

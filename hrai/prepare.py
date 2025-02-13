import pandas as pd
import time
import numpy as np

import combine
import elo1
import skills


def prepare(df):
    start_time = time.time()
    df = combine.clean(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    
    start_time = time.time()
    df = combine.un_vs_un(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    # df = elo1.calc_elo(df, 'ch_nom')
    # df = elo1.calc_elo(df, 'ch_driver')
    
    start_time = time.time()
    df = skills.calc_oskill(df)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    return df

df = pd.read_csv('./data/pmu2017.csv')
df = prepare(df)
df.to_csv('./data/pmu2017_os2.csv', index=False)
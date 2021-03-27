import pandas as pd
import datetime
import math
from progressbar import ProgressBar
from tqdm import tqdm
import numpy as np
import csv
import glob
import os

# date reference '2020/05/12'

def main():
    with open('./data/test/JAN20_bad.csv', newline='') as f:
        df = pd.read_csv('./data/test/JAN20_bad.csv', low_memory=False, skiprows=1,
                         names=['strike', 'datetime', 'open', 'high', 'low', 'close', 'expiry'])
    print(df)
    # df['expiry'] = pd.to_datetime(df.expiry, format='%d%b%y')
    # df['expiry'] = df.apply(lambda row: expiry(row), axis=1)format='%d%b%y'

    for index, row in df.iterrows():
        row['expiry'] = datetime.datetime.strptime(row['expiry'], '%d%b%y')
        row['expiry'] = int(row['expiry'].utcnow().timestamp())
    print(df)
    df.to_csv(r"C:\Users\AFEIAS\stock_py\data\test\JAN20_bad_res.csv")


if __name__ == "__main__":
    main()
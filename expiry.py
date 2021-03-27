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
    path_in = r'C:\Users\AFEIAS\stock_py\dataset\2018\September\Expiry 27th September'

    all_files = glob.glob(os.path.join(path_in, "*.csv"))
    names = [os.path.basename(x) for x in all_files]
    df = pd.DataFrame(columns = ['strike', 'date', 'time', 'open', 'high', 'low', 'close', 'volume'])

    for file_, name in zip(all_files, names):
        file_df = pd.read_csv(file_, names=['strike', 'date', 'time', 'open', 'high', 'low', 'close', 'volume'])
        # file_df['file_name'] = name
        file_df['expiry'] = '2018/09/27'
        df = df.append(file_df)
        
    print(df)
    df.to_csv(r"C:\Users\AFEIAS\stock_py\combined_dataset\2018\2018_35.csv")


if __name__ == "__main__":
    main()
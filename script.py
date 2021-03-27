import pandas as pd
import datetime
import math
from progressbar import ProgressBar
from tqdm import tqdm
import numpy as np
import csv

def expiry(row):
    x = row['strike']
    return x[-18:-11]

def main():
    pbar = ProgressBar()

    # v1
    # with open('./data/test/test_data.csv', newline='') as f:
    #     df = pd.read_csv('./data/test/test_data.csv', low_memory=False, skiprows=1,
    #                      names=['strike', 'date', 'time', 'open', 'high', 'low', 'close', 'volume', 'expiry'])

    with open('./data/2018/2018.csv', newline='') as f:
        df = pd.read_csv('./data/2018/2018.csv', low_memory=False, skiprows=1,
                         names=['strike', 'datetime', 'open', 'high', 'low', 'close', 'expiry'])
    
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df['expiry'] = pd.to_datetime(df.expiry, errors='coerce')

    with open('./ref/ref_2018.csv', newline='') as f:
        df_ref = pd.read_csv('./ref/ref_2018.csv', skiprows=6)
    
    df_ref.rename({"Unnamed: 3": "date",
                   "Unnamed: 4": "time", "Unnamed: 9": "strike",
                   "Unnamed: 10": "option_type", "Unnamed: 11": "expiry", },
                  axis="columns", inplace=True)
    print(df_ref)
    df_ref['datetime'] = pd.to_datetime(df_ref['date'] + ' ' + df_ref['time'])
    df_ref['datetime'] = df_ref['datetime'] + datetime.timedelta(minutes=14)
    df_ref['expiry'] = pd.to_datetime(df_ref.expiry, errors='coerce')
    

    df_opt_result = pd.DataFrame(
        columns=['Option Price', 'Trigger Price', 'SL', 'Target', 'Exit Price', 'Comments', 'Strike', 'Datetime', 'Price at 310'])
    print('Entering loop')

    with tqdm(total=df_ref.shape[0]) as pbar:    
        
        for index, ref_row in df_ref.iterrows():
            
            pbar.update(1)
            option_price = 0.0
            trigger_price = 0.0
            stop_loss = 0.0
            target = 0.0
            trigger_flag_1 = False
            trigger_flag_2 = False
            found_flag_2 = False
            exit_price = 0.0
            comments = ''
            
            df_temp = df.loc[(df['expiry'] == ref_row['expiry'])]
            closing_time_2 = datetime.datetime.combine(ref_row['datetime'].date(), datetime.time(15, 9, 00))
            print(df_temp)
            
            print(' Checking for ' + str(ref_row['strike']))

            for index, data_row in df_temp.iterrows():
                
                data_option_type = str(data_row['strike'][-6:-4])
                strike_data = str(data_row['strike'][-11:-6])
                
                strike_ref = str(ref_row['strike'])
                
                closing_time = datetime.datetime.combine(data_row['datetime'].date(), datetime.time(15, 9, 00))
               
                if(ref_row['datetime'] == data_row['datetime'] and data_option_type == ref_row['option_type'] and strike_ref == strike_data):
                    close_price = float(data_row['close'])
                    option_price = close_price
                    trigger_price = round_up(float(option_price)*1.16, 0.05)
                    stop_loss = round_down(float(trigger_price)*0.7, 0.05)
                    target = round_up(float(trigger_price)*1.6, 0.05)                    
                    trigger_flag_1 = True
                    row = (close_price, option_price, trigger_price, stop_loss, target, data_row['datetime'])
                    print(row)
                
                if(ref_row['datetime'].date() == data_row['datetime'].date() and data_option_type == ref_row['option_type'] and strike_ref == strike_data and trigger_flag_1 == True and float(data_row['high']) >= trigger_price):
                    trigger_flag_2 = True

                if(trigger_flag_2 == True and ref_row['datetime'].date() == data_row['datetime'].date() and data_option_type == ref_row['option_type'] and strike_ref == strike_data):
                    if(float(data_row['low']) <= stop_loss and float(data_row['high']) >= target and ref_row['datetime'].time() == data_row['datetime'].time()):
                        found_flag_2 = True
                        comments = 'Exception'
                        exit_price = 'Exception'
                        df_opt_result = print_rec(df_opt_result, option_price, trigger_price, stop_loss, target, exit_price, comments, ref_row['strike'], ref_row['datetime'], 0.0)
                        break
                    
                    if(float(data_row['low']) <= stop_loss):
                        found_flag_2 = True
                        exit_price = stop_loss
                        comments = 'SL'
                        df_opt_result = print_rec(df_opt_result, option_price, trigger_price, stop_loss, target, exit_price, comments, ref_row['strike'], ref_row['datetime'], 0.0)
                        break
                    
                    if(float(data_row['high']) >= target):
                        found_flag_2 = True
                        exit_price = target
                        comments = 'Target'                        
                        res = df_temp.loc[(df_temp['datetime'] == closing_time) & (df_temp['strike'] == data_row['strike'])]
                        row_list =[] 
                        for index, rows in res.iterrows():  
                            my_list =[rows.close]  
                            row_list.append(my_list)  
                        print(row_list) 
                        df_opt_result = print_rec(df_opt_result, option_price, trigger_price, stop_loss, target, exit_price, comments, ref_row['strike'], ref_row['datetime'], row_list[0][0])
                        break
                
                if(trigger_flag_2 == True and found_flag_2 == False):
                    try:
                       if(data_row['datetime'].time() == closing_time.time()):
                            exit_price = float(data_row['close'])
                            comments = 'Exit at 310'
                            df_opt_result = print_rec(df_opt_result, option_price, trigger_price, stop_loss, target, exit_price, comments, ref_row['strike'], ref_row['datetime'], 0.0)
                            break
                    except ValueError:
                        continue
                
                if(trigger_flag_1 == True and closing_time_2 <= data_row['datetime']):
                    break
                
            if(trigger_flag_2 == False and found_flag_2 == False and option_price != 0.0):
                exit_price = 0.0
                comments = 'No Trade'
                df_opt_result = print_rec(df_opt_result, option_price, trigger_price, stop_loss, target, exit_price, comments, ref_row['strike'], ref_row['datetime'], 0.0)
            
    print(df_opt_result)
    df_opt_result.to_csv(r'./results/2018/2018_res.csv')
                

def print_rec(df_opt_result, option_price, trigger_price, stop_loss, target, exit_price, comments, strike, datetime, price_at_310):
    with open('./results/2018/2018_res_1.csv','a') as f:
        writer=csv.writer(f)
        writer.writerow([
             option_price,
             trigger_price, 
             stop_loss, 
             target, 
             exit_price, 
             comments, 
             strike, 
             datetime, 
             price_at_310])
    return df_opt_result.append({'Option Price': option_price, 
                                'Trigger Price': trigger_price, 
                                'SL': stop_loss, 
                                'Target': target, 
                                'Exit Price': exit_price, 
                                'Comments': comments, 
                                'Strike': strike, 
                                'Datetime': datetime, 
                                'Price at 310': price_at_310}, ignore_index=True)

def round_down(x, a):
    return math.floor(x / a) * a


def round_up(x, a):
    return math.ceil(x / a) * a


def round_nearest(x, a):
    return round(x / a) * a


if __name__ == "__main__":
    main()
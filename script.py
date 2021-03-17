import pandas as pd
import datetime
import math


def main():
    with open('./data/weekly_options/test.csv', newline='') as f:
        df = pd.read_csv('./data/weekly_options/test.csv',
                         names=['strike', 'date', 'time', 'open', 'high', 'low', 'close', 'volume'])

    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    with open('./data/ref_2.csv', newline='') as f:
        df_ref = pd.read_csv('./data/ref_2.csv', skiprows=6)

    df_ref.rename({"Unnamed: 3": "date",
                   "Unnamed: 4": "time", "Unnamed: 9": "strike",
                   "Unnamed: 10": "option_type", "Unnamed: 11": "expiry", },
                  axis="columns", inplace=True)
    df_ref['datetime'] = pd.to_datetime(df_ref['date'] + ' ' + df_ref['time'])
    df_ref['datetime'] = df_ref['datetime'] + datetime.timedelta(minutes=15)

    df_result = pd.DataFrame(
        columns=['Option Price', 'Trigger Price', 'SL', 'Target', 'Exit Price', 'Comments'])

    for index, ref_row in df_ref.iterrows():

        option_price = ''
        trigger_price = 0.0
        stop_loss = ''
        target = ''

        for index, data_row in df.iterrows():

            data_option_type = data_row['strike'][-4:]

            if(ref_row['datetime'] == data_row['datetime'] and data_option_type == ref_row['option_type']):
                # also match expiry from folder
                print(df_result)

                close_price = data_row['close']
                option_price = close_price
                trigger_price = round_up(float(option_price)*1.16)
                stop_loss = round_down(float(trigger_price)*0.7)
                target = round_up(float(trigger_price)*1.6)
                df_result = df_result.append({'Option Price': option_price,
                                              'Trigger Price': trigger_price,
                                              'SL': stop_loss,
                                              'Target': target,
                                              'Exit Price': '',
                                              'Comments': ''}, ignore_index=True)
                print(df_result)
                # if: ref_row date should match data_row date
                #   if: ref_row['time'] + 15 min == data_row['time'] (adjust time formats)
                #       close_price = data_row['close']
                #       option_price = close_price
                #       trigger_price = option_price*1.16 (round off upper side 0.05 multiple) two decimal upper limit
                #       stop_loss = trigger_price*0.7 (round off down side 0.05 multiple) two decimal down limit\
                #       target = trigger_price*1.6 (round off upper side 0.05 multiple) two decimal upper limit
                # if(ref_row['date'] != row['date']):
                # print('hellow')


def round_down(x, a):
    return math.floor(x / a) * a


def round_up(x, a):
    return math.ceil(x / a) * a


def round_nearest(x, a):
    return round(x / a) * a


if __name__ == "__main__":
    main()

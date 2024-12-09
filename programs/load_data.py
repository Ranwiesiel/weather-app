import pandas as pd
import datetime

def get_time(data, time=datetime.datetime.now()):
    current_date = time.strftime("%Y-%m-%d %H")
    return data[data['date'] == current_date]

def get_data(data):
    df = pd.read_csv(data, parse_dates=[0])
    df.rename(columns={df.columns[0]: 'date'}, inplace=True)
    df['date'] = df['date'].dt.strftime("%Y-%m-%d %H")
    df = get_time(df)
    timeseries = df.date.values
    temp = df.predicted_mean.values
    return timeseries, temp

def get_data_all(data):
    df = pd.read_csv(data, parse_dates=[0])
    df.rename(columns={df.columns[0]: 'date'}, inplace=True)
    df['date'] = df['date'].dt.strftime("%Y-%m-%d jam %H")
    timeseries = df.date.values
    temp = df.predicted_mean.values
    return timeseries, temp

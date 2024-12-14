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
    df['years'] = df['date'].dt.strftime("%Y")
    df['months'] = df['date'].dt.strftime("%m")
    df['days'] = df['date'].dt.strftime("%A")
    df['daysn'] = df['date'].dt.strftime("%d")
    df['hours'] = df['date'].dt.strftime("%H").astype(int)
    df['temp'] = df.predicted_mean.values.astype(int)
    df = df[df['hours'] % 3 == 0]
    return df.drop(columns=['predicted_mean'])

def to_dict(df):
	data_dict = {}

	# Loop through years
	for year in df['years'].unique():
		data_dict[year] = {}
		
		# Filter data for the current year
		year_data = df[df['years'] == year]
		
		# Loop through months
		for month in year_data['months'].unique():
			data_dict[year][month] = {}
			
			# Filter data for the current month
			month_data = year_data[year_data['months'] == month]
			
			# Loop through unique dates
			for date in month_data['daysn'].unique():
				data_dict[year][month][date] = {}
				
				# Filter data for the current date
				date_data = month_data[month_data['daysn'] == date]
				# Get the name of the day
				day_name = date_data['days'].values[0]
				data_dict[year][month][date]['day_name'] = day_name
				
				# Loop through the hours and store the corresponding temperature
				for hour in date_data['hours'].unique():
					temp = date_data[date_data['hours'] == hour]['temp'].values[0]
					data_dict[year][month][date][hour] = temp

	return data_dict
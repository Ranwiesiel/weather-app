import requests
from datetime import datetime
import pandas as pd
import joblib



def predict_sby():
    api = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Surabaya,ID/today?unitGroup=metric&include=hours&key=AQCL3EG5SNW9XDN44A67J95UB'

    response = requests.get(api)

    if response.status_code == 200:
        weather_data = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)    

    
    rounded_current_hour = datetime.now().replace(minute=0, second=0, microsecond=0).strftime('%H:%M:%S')  # Misal: '01:00:00'

    print(f"Rounded current hour: {rounded_current_hour}")
    selected_hour = next((hour for hour in weather_data['days'][0]['hours'] if hour['datetime'] == rounded_current_hour), None)

    sby_weather = pd.DataFrame(selected_hour, index=[0])
    df_tes = sby_weather.copy()
    df_tes.drop(columns=['snowdepth', 'snow', 'preciptype', 'precipprob', 'precip', 'datetime', 'icon', 'stations', 'source', 'datetime', 'datetimeEpoch', 'solarradiation', 'solarenergy', 'uvindex' , 'severerisk', 'pressure'], inplace=True)
    label_mapping = {
        'Partially cloudy': 'Cloudy',
        'Rain, Partially cloudy': 'Rain',
        'Overcast': 'Cloudy',
        'Rain, Overcast': 'Rain',
        'Clear': 'Clear',
        'Rain': 'Rain'
    }
    # Mengganti label pada kolom 'conditions'
    df_tes['conditions'] = df_tes['conditions'].map(label_mapping)

    label_encoder = joblib.load('data/predict/label_encoder.pkl')
    model = joblib.load('data/predict/model_rf.pkl')
    df_tes['conditions'] = label_encoder.transform(df_tes['conditions'])

    df_tes = df_tes[['temp', 'feelslike', 'dew', 'humidity', 'windgust', 'windspeed',
    'winddir', 'cloudcover', 'visibility']]
    
    predicted_class_origin = model.predict(df_tes)

    predicted_class_decode = label_encoder.inverse_transform(predicted_class_origin.reshape(-1))

    if predicted_class_decode[0] == 'Cloudy':
        pred_logo = 'static/sun-cloudy.png'
        pred_color = '#BCCCDC'
        pred_rgb = 'rgb(188, 204, 220, 0,2)'
        pred_icon = 'fa-solid fa-cloud'
    elif predicted_class_decode[0] == 'Clear':
        pred_logo = 'static/sun.png'
        pred_color = '#B1F0F7'
        pred_rgb = 'rgb(177, 240, 247, 0,2)'
        pred_icon = 'fa-solid fa-sun'
    elif predicted_class_decode[0] == 'Rain':
        pred_logo = 'static/rain.png'
        pred_color = '#63839c'
        pred_rgb = 'rgb(99, 131, 156, 0,2)'
        pred_icon = 'fa-solid fa-cloud-showers-heavy'


    return predicted_class_decode[0], pred_logo, pred_color, pred_rgb, df_tes, pred_icon


def predict_bangkalan():
    api = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Bangkalan,ID/today?unitGroup=metric&include=hours&key=AQCL3EG5SNW9XDN44A67J95UB'

    response = requests.get(api)

    if response.status_code == 200:
        weather_data = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)    

    
    rounded_current_hour = datetime.now().replace(minute=0, second=0, microsecond=0).strftime('%H:%M:%S')  # Misal: '01:00:00'

    print(f"Rounded current hour: {rounded_current_hour}")
    selected_hour = next((hour for hour in weather_data['days'][0]['hours'] if hour['datetime'] == rounded_current_hour), None)

    sby_weather = pd.DataFrame(selected_hour, index=[0])
    df_tes = sby_weather.copy()
    df_tes.drop(columns=['snowdepth', 'snow', 'preciptype', 'precipprob', 'precip', 'datetime', 'icon', 'stations', 'source', 'datetime', 'datetimeEpoch', 'solarradiation', 'solarenergy', 'uvindex' , 'severerisk', 'pressure'], inplace=True)
    label_mapping = {
        'Partially cloudy': 'Cloudy',
        'Rain, Partially cloudy': 'Rain',
        'Overcast': 'Cloudy',
        'Rain, Overcast': 'Rain',
        'Clear': 'Clear',
        'Rain': 'Rain'
    }
    # Mengganti label pada kolom 'conditions'
    df_tes['conditions'] = df_tes['conditions'].map(label_mapping)

    label_encoder = joblib.load('data/predict/label_encoder_bgkln.pkl')
    model = joblib.load('data/predict/model_rf_bgkln.pkl')
    df_tes['conditions'] = label_encoder.transform(df_tes['conditions'])

    df_tes = df_tes[['temp', 'feelslike', 'dew', 'humidity', 'windgust', 'windspeed',
    'winddir', 'cloudcover', 'visibility']]
    
    predicted_class_origin = model.predict(df_tes)

    predicted_class_decode = label_encoder.inverse_transform(predicted_class_origin.reshape(-1))

    if predicted_class_decode[0] == 'Cloudy':
        pred_logo = 'static/sun-cloudy.png'
        pred_color = '#BCCCDC'
        pred_rgb = 'rgb(188, 204, 220, 0,2)'
        pred_icon = 'fa-solid fa-cloud'
    elif predicted_class_decode[0] == 'Clear':
        pred_logo = 'static/sun.png'
        pred_color = '#B1F0F7'
        pred_rgb = 'rgb(177, 240, 247, 0,2)'
        pred_icon = 'fa-solid fa-sun'
    elif predicted_class_decode[0] == 'Rain':
        pred_logo = 'static/rain.png'
        pred_color = '#63839c'
        pred_rgb = 'rgb(99, 131, 156, 0,2)'
        pred_icon = 'fa-solid fa-cloud-showers-heavy'


    return predicted_class_decode[0], pred_logo, pred_color, pred_rgb, df_tes, pred_icon
    
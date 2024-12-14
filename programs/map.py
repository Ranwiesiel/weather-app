import folium
from .load_data import *


# Data Forecast
bkl_data = 'data/forecast/bkl_temp_forecast.csv'
sby_data = 'data/forecast/sby_temp_forecast.csv'


# Generate map
sby_coords = [-7.246, 112.738]
bkl_coords = [-7.030, 112.747]

map = folium.Map(location=[-7.169,112.779], zoom_start=11, max_zoom=16, min_zoom=10,
                 tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
                 attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors & <a href="https://carto.com/attributions">CARTO</a>'
)

def get_forecast_data():
    sby_timeseries, sby_temp = get_data(sby_data)
    bkl_timeseries, bkl_temp = get_data(bkl_data)
    return\
        sby_timeseries, sby_temp,\
        bkl_timeseries, bkl_temp

def get_combined_data():
    sby_data_all = to_dict(get_data_all(bkl_data))
    bkl_data_all = to_dict(get_data_all(bkl_data))
    return\
        sby_data_all, \
        bkl_data_all
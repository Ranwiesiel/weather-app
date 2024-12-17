from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from programs.map import *
from programs.predict_cuaca import *
from datetime import datetime
import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import requests
import sys
import pandas as pd
import json
import joblib

app = Flask(__name__)


model = load_model('data/model/cnnModel.keras')

# Tentukan ukuran gambar yang dibutuhkan oleh model
img_width, img_height = 256, 256

# Tentukan direktori penyimpanan gambar yang diupload
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/', methods=['POST', 'GET'])
def home():
    sby_timeseries, sby_temp, bkl_timeseries, bkl_temp = get_forecast_data()
    sby_data, bkl_data = get_combined_data()
    
    filename = ''
    predicted_class = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Simpan gambar yang diupload
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Proses gambar untuk prediksi
            img = Image.open(file_path).convert('RGB')
            img = img.resize((img_width, img_height))
            img_array = np.array(img) / 255.0  # Normalisasi gambar
            img_array = np.expand_dims(img_array, axis=0)  # Tambahkan dimensi batch
            
            prediction = model.predict(img_array)
            class_idx = np.argmax(prediction, axis=1)[0]

            class_names = ['Berawan', 'Berkabut', 'Hujan', 'Cerah', 'Sunrise']
            predicted_class = class_names[class_idx]
        
    return render_template('index.html',
                        h_now=datetime.now().strftime('%H'),
                        d_now=datetime.now().strftime('%d'),
                        dname_now=datetime.now().strftime('%A'),

                        sby_timeseries=sby_timeseries,
                        sby_temp=sby_temp,
                        bkl_timeseries=bkl_timeseries,
                        bkl_temp=bkl_temp,

                        sby_data=sby_data,
                        bkl_data=bkl_data,
                        
                        filename=filename, predicted_class=predicted_class
                        )

@app.route('/cuaca', methods=['POST', 'GET'])
def prediksi_cuaca():
    wilayah = request.args.get('wilayah')
    filename = ''
    predicted_class = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Simpan gambar yang diupload
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Proses gambar untuk prediksi
            img = Image.open(file_path).convert('RGB')
            img = img.resize((img_width, img_height))
            img_array = np.array(img) / 255.0  # Normalisasi gambar
            img_array = np.expand_dims(img_array, axis=0)  # Tambahkan dimensi batch
            
            prediction = model.predict(img_array)
            class_idx = np.argmax(prediction, axis=1)[0]

            class_names = ['Berawan', 'Berkabut', 'Hujan', 'Cerah', 'Sunrise']
            predicted_class = class_names[class_idx]


    if request.method == 'GET':
        if not wilayah:
            return redirect('/cuaca?wilayah=surabaya')
        if wilayah.lower() == "surabaya":
            pred_class_weather, pred_logo_weather, pred_color_weather, pred_rgb_weather , df_weather, pred_icon_weather = predict_sby()
            json_sby = 'data/predict/3578.json'
            with open(json_sby) as f:
                json_geo = json.load(f)
                json_coor1 = -7.2890784
                json_coor2 = 112.7786537

        if wilayah.lower() == "bangkalan":
            pred_class_weather, pred_logo_weather, pred_color_weather, pred_rgb_weather , df_weather, pred_icon_weather = predict_bangkalan()
            json_bkl = 'data/predict/3526.json'
            with open(json_bkl) as f:
                json_geo = json.load(f)
                json_coor1 = -7.0416324
                json_coor2 = 112.9204642
        
        if wilayah.lower() not in ['surabaya', 'bangkalan']:
            return redirect('/cuaca?wilayah=surabaya')


        
    return render_template('prediksi_cuaca.html',
                        h_now=datetime.now().strftime('%H'),
                        d_now=datetime.now().strftime('%d'),
                        dname_now=datetime.now().strftime('%A'),
                        pred_class_weather=pred_class_weather,
                        pred_logo_weather=pred_logo_weather,
                        pred_color_weather=pred_color_weather,
                        pred_rgb_weather=pred_rgb_weather,
                        df_weather=df_weather,
                        pred_icon_weather=pred_icon_weather,
                        json_geo=json_geo,
                        json_coor1=json_coor1,
                        json_coor2=json_coor2,
                        filename=filename, predicted_class=predicted_class
                        )

@app.route("/cluster", methods=['POST', 'GET'])
def hello():
    peta_persebaran = folium.Map(location=[-2.5, 118], zoom_start=5)

    df = pd.read_csv('data/cluster/climate_data_clustered.csv')

    colors = ['red', 'yellow', 'green']

    risk_mapping = {'low risk': 0 , 'medium risk': 1, 'high risk': 2 }

    y_kmeans = df['cluster'].map(risk_mapping)

    # Tambahkan kluster ke peta
    for i in range(len(y_kmeans)):
        clusternya = y_kmeans[i]
        
        folium.CircleMarker(
            location=[-7.2053, 112.7353], 
            radius=13,            
            color=colors[clusternya], 
            fill=True,               
            fill_color=colors[clusternya],
            fill_opacity=0.1,          
        ).add_to(peta_persebaran)

    peta_persebaran.save('./templates/peta_persebaran.html')
    data = df.to_html(classes='table table-striped')
    return render_template('index_cluster.html', dataframe=data)

if __name__ == '__main__':
    import os
    os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0', port=8001, debug=True)
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from programs.map import *
from datetime import datetime
import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

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

# @app.route('/map')
# def map():
#     return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
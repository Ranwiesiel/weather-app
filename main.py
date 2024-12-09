from flask import Flask, redirect, url_for, render_template
from programs.map import generate_map

app = Flask(__name__)

@app.route('/')
def home():
    generate_map()
    return render_template('map.html')


    # return redirect(url_for('map'))

# @app.route('/map')
# def map():
#     return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
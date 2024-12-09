import folium
import re
import json
from .load_data import get_data, get_data_all

# Data Forecast
bkl_data = 'data/forecast/bkl_temp_forecast.csv'
sby_data = 'data/forecast/sby_temp_forecast.csv'

sby_coords = [-7.246, 112.738]
bkl_coords = [-7.030, 112.747]

map = folium.Map(location=[-7.169,112.779], zoom_start=11, max_zoom=16, min_zoom=10,
                 tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
                 attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors & <a href="https://carto.com/attributions">CARTO</a>'
                )


def custom_code(region, celcius, map, date_data, temp_data):
    date_data_json = json.dumps(date_data.tolist())
    temp_data_json = json.dumps(temp_data.tolist())

    return f'''
    
        var marker = L.marker(
            [{region[0]}, {region[1]}],
            {{}}
        ).addTo({map});

        var div_icon = L.divIcon({{"className": "empty", "html": "<div style='font-size: 14px; color: black;'><b>{region[2]} {celcius:.2f}℃</b></div>"}});  // Rounded to 2 decimal places
        marker.setIcon(div_icon);

        marker.on('click', function() {{
            let tempData = getTemperatureDataForRegion({date_data_json}, {temp_data_json});

            document.getElementById('tempTitle').innerHTML = "<b>{region[2]} Temperature Info</b>";

            // Populate the 24-hour forecast
            let forecastList = document.getElementById('forecastList');
            forecastList.innerHTML = '';  // Clear previous list
            tempData.forecast.forEach(function(temp, index) {{
                let li = document.createElement('li');
                li.innerHTML = tempData.date[index] + ": <b>" + temp.toFixed(2) + "℃</b>";  // Rounded to 2 decimal places
                forecastList.appendChild(li);
            }});

            $('#tempModal').modal('show');
        }});

        function getTemperatureDataForRegion(dateData, tempData) {{
            let forecast = tempData;

            return {{
                forecast: forecast,
                date: dateData
            }};
        }}
    '''


def add_modal_to_html(html):
    modal_html = '''
    <div class="modal" tabindex="-1" id="tempModal" style="display: none;">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title" id="tempTitle"></h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            </div>
            <div class="modal-body">
            <div id="tempDetails">
                <h6>Desember 24-hour forecast:</h6>
                <ul id="forecastList"></ul>
            </div>
            </div>
        </div>
        </div>
    </div>
    '''
    body_end_index = html.rfind('</body>')
    return html[:body_end_index] + modal_html + html[body_end_index:]


def generate_map():
    _, temp_sby = get_data(sby_data)
    _, temp_bkl = get_data(bkl_data)

    all_date_sby, all_temp_sby = get_data_all(sby_data)
    all_date_bkl, all_temp_bkl = get_data_all(bkl_data)

    map.save('templates/map.html')

    with open('templates/map.html', 'r', encoding='utf-8') as file:
        html = file.read()

    html = add_modal_to_html(html)
    
    map_var_match = re.search(r'var (map_[a-z0-9]+) = L\.map', html)
    if map_var_match:
        map_var = map_var_match.group(1)

    sby_code = custom_code(sby_coords + ['Surabaya'], temp_sby.item(), map_var, all_date_sby, all_temp_sby)
    bkl_code = custom_code(bkl_coords + ['Bangkalan'], temp_bkl.item(), map_var, all_date_bkl, all_temp_bkl)
    pstart = html.find('tile_layer')
    pend = html.find('</script>', pstart)

    with open('templates/map.html', 'w', encoding='utf-8') as file:
        file.write(
            html[:pend] +
            f'{sby_code}' +
            f'{bkl_code}' +
            html[pend:]
        ) 
from flask import Flask, render_template, request
import requests
import os

api_key = os.environ.get("API_KEY")
base_url = "https://api.weatherapi.com/v1/forecast.json"
app = Flask(__name__)
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/help_')
def help_():
    return render_template("help.html")
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip().lower()
    print(query)
    if not query:
        return render_template("error.html",error_code = "N/A")
    found_items = []
    for name in ski_resorts_top100.keys():
        if query in name.lower():
            print("Match")
            found_items.append(name)
    return render_template("search_result.html",results = found_items)
@app.route('/api')
def api():
    location = request.args.get("location","Thredbo")
    print(location)
    coords = ski_resorts_top100.get(location)
    coords_ = f"{coords[0]},{coords[1]}"
    return get_weather(coords_,location)
# AI MADE list of top ski resorts with coords 

ski_resorts_top100 = {
    # --- Australia ---
    "Perisher (Australia)": (-36.405, 148.411),
    "Thredbo (Australia)": (-36.500, 148.317),
    "Falls Creek (Australia)": (-36.865, 147.278),
    "Mt Buller (Australia)": (-37.146, 146.450),
    "Mt Hotham (Australia)": (-36.980, 147.133),
    "Selwyn (Australia)": (-35.770, 148.660),
    "Charlotte Pass (Australia)": (-36.431, 148.328),
    "Dinner Plain (Australia)": (-37.033, 147.183),
    "Mt Stirling (Australia)": (-37.033, 146.450),
    "Ben Lomond (Australia)": (-41.533, 147.233),
    "Mt Mawson (Australia)": (-42.750, 146.583),
    "Corin Forest (Australia)": (-35.433, 148.883),

    # --- Japan ---
    "Niseko United (Japan)": (42.804, 140.687),
    "Hakuba Valley (Japan)": (36.700, 137.850),
    "Furano (Japan)": (43.350, 142.350),
    "Nozawa Onsen (Japan)": (36.916, 138.450),
    "Shiga Kogen (Japan)": (36.730, 138.500),
    "Myoko Kogen (Japan)": (36.900, 138.183),
    "Rusutsu (Japan)": (42.750, 140.900),
    "Zao Onsen (Japan)": (38.170, 140.450),
    "Appi Kogen (Japan)": (40.000, 141.250),
    "Naeba (Japan)": (36.800, 138.750),

    # --- North America ---
    "Whistler Blackcomb (Canada)": (50.115, -122.945),
    "Lake Louise (Canada)": (51.425, -116.177),
    "Sun Peaks (Canada)": (50.883, -119.883),
    "Revelstoke (Canada)": (51.000, -118.167),
    "Banff Sunshine (Canada)": (51.115, -115.783),
    "Big White (Canada)": (49.700, -119.083),
    "Mont Tremblant (Canada)": (46.210, -74.580),
    "Vail (USA)": (39.640, -106.374),
    "Aspen (USA)": (39.208, -106.949),
    "Breckenridge (USA)": (39.481, -106.038),
    "Telluride (USA)": (37.937, -107.812),
    "Jackson Hole (USA)": (43.587, -110.827),
    "Park City (USA)": (40.651, -111.509),
    "Mammoth Mountain (USA)": (37.630, -119.032),
    "Heavenly (USA)": (38.950, -119.940),
    "Squaw Valley / Palisades Tahoe (USA)": (39.200, -120.233),
    "Steamboat (USA)": (40.459, -106.805),
    "Deer Valley (USA)": (40.622, -111.478),
    "Snowbird (USA)": (40.581, -111.654),
    "Alta (USA)": (40.588, -111.638),
    "Killington (USA)": (43.677, -72.779),
    "Stowe (USA)": (44.465, -72.687),

    # --- Europe (Alps & beyond) ---
    "Chamonix (France)": (45.923, 6.869),
    "Zermatt (Switzerland)": (46.020, 7.749),
    "St. Anton (Austria)": (47.128, 10.268),
    "Verbier (Switzerland)": (46.095, 7.228),
    "Val d’Isère (France)": (45.448, 6.980),
    "Les 3 Vallées (France)": (45.400, 6.600),
    "Courchevel (France)": (45.415, 6.634),
    "La Plagne (France)": (45.510, 6.678),
    "Ischgl (Austria)": (47.012, 10.291),
    "Kitzbühel (Austria)": (47.444, 12.392),
    "Sölden (Austria)": (46.970, 11.010),
    "Davos-Klosters (Switzerland)": (46.800, 9.833),
    "Grindelwald (Switzerland)": (46.624, 8.042),
    "Saas-Fee (Switzerland)": (46.110, 7.930),
    "Tignes (France)": (45.470, 6.910),
    "Alpe d’Huez (France)": (45.090, 6.070),
    "Laax (Switzerland)": (46.800, 9.250),
    "Livigno (Italy)": (46.533, 10.133),
    "Cortina d’Ampezzo (Italy)": (46.540, 12.135),
    "Madonna di Campiglio (Italy)": (46.230, 10.830),
    "Andermatt (Switzerland)": (46.633, 8.600),
    "Garmisch-Partenkirchen (Germany)": (47.500, 11.100),
    "Sierra Nevada (Spain)": (37.093, -3.397),
    "Bansko (Bulgaria)": (41.838, 23.488),
    "Poiana Brașov (Romania)": (45.617, 25.550),
    "Les Arcs (France)": (45.572, 6.781),
    "Meribel (France)": (45.410, 6.565),
    "Avoriaz (France)": (46.190, 6.770),
    "La Clusaz (France)": (45.880, 6.430),
    "Megève (France)": (45.850, 6.617),
    "Chamrousse (France)": (45.100, 5.883),
    "Val Thorens (France)": (45.300, 6.583),

    # --- Scandinavia & Eastern Europe ---
    "Åre (Sweden)": (63.399, 13.082),
    "Hemsedal (Norway)": (60.859, 8.538),
    "Trysil (Norway)": (61.311, 12.264),
    "Ruka (Finland)": (66.167, 29.167),
    "Levi (Finland)": (67.800, 24.800),
    "Gudauri (Georgia)": (42.480, 44.480),

    # --- South America ---
    "Valle Nevado (Chile)": (-33.350, -70.250),
    "Portillo (Chile)": (-32.833, -70.123),
    "La Parva (Chile)": (-33.350, -70.300),
    "Cerro Catedral (Argentina)": (-41.167, -71.500),
    "Las Leñas (Argentina)": (-35.150, -70.050),
}

def get_weather(location,name):
    params = {
        "key":api_key,
        "q":location,
        "days": 3,
    }
    response = requests.get(base_url,params=params)
    if response.status_code == 200:
        data = simplify_data(response.json())
        data["Query_location"] = name
        data["query_coords"] = location
        return render_template("api_result.html",**data)
    # Check for "error"
    else:
        print("Error Occured")
        return render_template('error.html',error_code=response.status_code)

def simplify_data(data):
    if data:
        forecast_day = data["forecast"]["forecastday"][0]
        hourly_list = []
        for hour in  data["forecast"]["forecastday"][0]["hour"]:
            hourly_list.append({
                "time": hour["time"],
                "temperature": hour["temp_c"],
                "feels_like": hour["feelslike_c"],
                "windchill": hour["windchill_c"],
                "condition": hour["condition"]["text"],
                "condition_icon": hour["condition"]["icon"],
                "wind_speed": hour["wind_kph"],
                "wind_dir": hour["wind_dir"],
                "precipitation": hour["precip_mm"],
                "snow": hour["temp_c"],
                "chancerain": hour["chance_of_rain"],
                "chancesnow": hour["chance_of_snow"],
                "vis_km": hour["vis_km"],
                "humidity": hour["humidity"],
                "uv": hour["uv"],
            })
        new_data = {
            "location":data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "coords":f"{data['location']['lat']}, {data['location']['lon']}",
            "last_updated":data["current"]["last_updated"],
            # Current Infomation
            "local_time":data["location"]["localtime"],
            "current_temperature": data["current"]["temp_c"] ,
            "currrent_feels_like": data["current"]["feelslike_c"] ,
            "currrent_windchill": data["current"]["windchill_c"] ,
            "current_condition": data["current"]["condition"]["text"],
            "current_condition_icon":data["current"]["condition"]["icon"],
            "current_wind_speed":data["current"]["wind_kph"],
            "current_wind_dir":data["current"]["wind_dir"],
            "current_precipatation":data["current"]["precip_mm"],
            "current_vis_km": data["current"]["vis_km"],
            "current_humidity":data["current"]["humidity"],
            "current_uv": data["current"]["uv"],
            # Forecast Day
            "date_of_day": forecast_day["date"],
            "sunrise": forecast_day["astro"]["sunrise"],
            "sunset": forecast_day["astro"]["sunset"],
            "day_condition": forecast_day["day"]["condition"]["text"],
            "day_icon": forecast_day["day"]["condition"]["icon"],
            "max_temp": forecast_day["day"]["maxtemp_c"],
            "min_temp": forecast_day["day"]["mintemp_c"],
            "avg_temp": forecast_day["day"]["avgtemp_c"],
            "max_wind_kph": forecast_day["day"]["maxwind_kph"],
            "average_vis": forecast_day["day"]["avgvis_km"],
            "uv": forecast_day["day"]["uv"],
            "daily_chance_rain": forecast_day["day"]["daily_chance_of_rain"],
            "daily_chance_snow": forecast_day["day"]["daily_chance_of_snow"],
            "total_precip": forecast_day["day"]["totalprecip_mm"],
            "totalsnow_cm": forecast_day["day"]["totalsnow_cm"],
            # Hour by hour breakdown
            "hourly":hourly_list
         }
        return new_data
    else:
        return None

if __name__ == '__main__':
    app.run(debug=False)
import requests
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
import os

apikey = os.environ['api_key']
cred = credentials.Certificate({
    "type":
    "service_account",
    "project_id":
    os.environ['project_id'],
    "private_key_id":
    os.environ['private_key_id'],
    "private_key":
    os.environ['private_key'],
    "client_email":
    os.environ['client_email'],
    "client_id":
    os.environ['client_id'],
    "auth_uri":
    os.environ['auth_uri'],
    "token_uri":
    os.environ['token_uri'],
    "auth_provider_x509_cert_url":
    os.environ['auth_provider_x509_cert_url'],
    "client_x509_cert_url":
    os.environ['client_x509_cert_url'],
    "universe_domain":
    os.environ['universe_domain']
})

firebase_admin.initialize_app(cred)


def convert_to_lower_no_spaces(s):
  return s.lower().replace(" ", "")


def get_air():
  api_url = "http://api.weatherapi.com/v1/current.json"
  aqi = "yes"
  city_names = []
  with open('city_zip.txt', 'r') as file:
    for line in file:
      city_names.append(line.strip())
  count = 0
  for location in city_names:
    params = {"key": apikey, "q": location, "aqi": aqi}

    try:
      response = requests.get(api_url, params=params)

      if response.status_code == 200:
        data = response.json()

        location = data['location']
        current = data['current']
        name = location['name']
        country = location['country']
        lon = location['lon']
        lat = location['lat']
        localtime = location['localtime']
        localtime_datetime = datetime.strptime(localtime, "%Y-%m-%d %H:%M")
        date = localtime_datetime.strftime("%Y-%m-%d")
        time = localtime_datetime.strftime("%H:%M")
        temp_c = current['temp_c']
        temp_f = current['temp_f']
        condition_text = current['condition']['text']
        wind_kph = current['wind_kph']
        wind_degree = current['wind_degree']
        wind_dir = current['wind_dir']
        pressure_mb = current['pressure_mb']
        precip_mm = current['precip_mm']
        humidity = current['humidity']
        cloud = current['cloud']
        vis_km = current['vis_km']
        uv = current['uv']
        gust_kph = current['gust_kph']

        air_quality = current['air_quality']
        if air_quality != {}:
          count += 1
          co = air_quality['co']
          no2 = air_quality['no2']
          o3 = air_quality['o3']
          so2 = air_quality['so2']
          pm2_5 = air_quality['pm2_5']
          pm10 = air_quality['pm10']
          us_epa_index = air_quality['us-epa-index']
          gb_defra_index = air_quality['gb-defra-index']
          extracted_data = {
              "name": convert_to_lower_no_spaces(name),
              "country": convert_to_lower_no_spaces(country),
              "latitude": lat,
              "longitude": lon,
              "date": date,
              "time": time,
              "temperature_c": temp_c,
              "temperature_f": temp_f,
              "condition": convert_to_lower_no_spaces(condition_text),
              "wind_speed_kph": wind_kph,
              "wind_degree": wind_degree,
              "wind_direction": convert_to_lower_no_spaces(wind_dir),
              "pressure_mb": pressure_mb,
              "precipitation_mm": precip_mm,
              "humidity": humidity,
              "cloud_cover": cloud,
              "visibility_km": vis_km,
              "uv_index": uv,
              "gust_speed_kph": gust_kph,
              "co": co,
              "no2": no2,
              "o3": o3,
              "so2": so2,
              "pm2_5": pm2_5,
              "pm10": pm10,
              "us_epa_index": us_epa_index,
              "gb_defra_index": gb_defra_index
          }
          db = firestore.client()
          doc_ref = db.collection('hourlyData').document()
          doc_ref.set(extracted_data)
          print(name, " Document ID:", doc_ref.id, "@ Time: ", time)

      else:
        print(
            f"Request for {location} failed with status code: {response.status_code}"
        )
    except requests.RequestException as e:
      print(f"Request for {location} failed: {e}")

  print(f"{count} locations processed")


app = Flask(__name__)


@app.route('/')
def hello():
  get_air()
  return 'Storing Records!'


app.run(host='0.0.0.0')

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import csv
from datetime import datetime
import os

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

db = firestore.client()
collection_ref = db.collection('hourlyData')

current_date = datetime.now().strftime('%Y-%m-%d')
csv_file_name = f'firestore_{current_date}.csv'

header = [
    'Document ID', 'date', 'time', 'name', 'country', 'latitude', 'longitude',
    'temperature_c', 'temperature_f', 'condition', 'wind_speed_kph',
    'wind_degree', 'wind_direction', 'gust_speed_kph', 'pressure_mb',
    'precipitation_mm', 'humidity', 'visibility_km', 'uv_index', 'cloud_cover',
    'o3', 'co', 'no2', 'so2', 'pm2_5', 'pm10', 'gb_defra_index', 'us_epa_index'
]

csv_file = open(csv_file_name, 'w', newline='')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(header)

docs = collection_ref.stream()

for doc in docs:
  doc_data = doc.to_dict()
  row = [
      doc.id,
      doc_data.get('date', ''),
      doc_data.get('time', ''),
      doc_data.get('name', ''),
      doc_data.get('country', ''),
      doc_data.get('latitude', ''),
      doc_data.get('longitude', ''),
      doc_data.get('temperature_c', ''),
      doc_data.get('temperature_f', ''),
      doc_data.get('condition', ''),
      doc_data.get('wind_speed_kph', ''),
      doc_data.get('wind_degree', ''),
      doc_data.get('wind_direction', ''),
      doc_data.get('gust_speed_kph', ''),
      doc_data.get('pressure_mb', ''),
      doc_data.get('precipitation_mm', ''),
      doc_data.get('humidity', ''),
      doc_data.get('visibility_km', ''),
      doc_data.get('uv_index', ''),
      doc_data.get('cloud_cover', ''),
      doc_data.get('o3', ''),
      doc_data.get('co', ''),
      doc_data.get('no2', ''),
      doc_data.get('so2', ''),
      doc_data.get('pm2_5', ''),
      doc_data.get('pm10', ''),
      doc_data.get('gb_defra_index', ''),
      doc_data.get('us_epa_index', '')
  ]

  csv_writer.writerow(row)

csv_file.close()

print(f"Data exported to '{csv_file_name}'")

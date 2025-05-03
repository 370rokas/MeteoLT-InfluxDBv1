import requests, os
from influxdb import InfluxDBClient
from datetime import datetime
import schedule
import time

# Get environment variables
STATION_ID = os.environ.get("STATION_ID", "")
SCHEDULER_INTERVAL = int(os.environ.get("SCHEDULER_INTERVAL", "0"))

INFLUXDB_MEASUREMENT = os.environ.get("INFLUXDB_MEASUREMENT", "weather")
INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "localhost")
INFLUXDB_PORT = int(os.environ.get("INFLUXDB_PORT", 8086))
INFLUXDB_DATABASE = os.environ.get("INFLUXDB_DATABASE", "")
INFLUXDB_USERNAME = os.environ.get("INFLUXDB_USERNAME", "")
INFLUXDB_PASSWORD = os.environ.get("INFLUXDB_PASSWORD", "")

def getWeatherData(stationID: str) -> dict | None:
    """
    This function fetches the latest weather observations from the Meteo.lt API for a given station ID
    """
    res = requests.get(f"https://api.meteo.lt/v1/stations/{stationID}/observations/latest")

    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to fetch weather data. Status code: {res.status_code}")
        return None

def pushDataToInfluxDB(stationCode: str, data: dict):
    """
    This function pushes the weather data to InfluxDB
    """
    client = InfluxDBClient(
        host=INFLUXDB_HOST,
        port=INFLUXDB_PORT,
        username=INFLUXDB_USERNAME,
        password=INFLUXDB_PASSWORD
    )
    client.switch_database(INFLUXDB_DATABASE)

    json_body = []

    for measurement in data:
        observationTimeUtc: str = measurement["observationTimeUtc"]  # sample: "2025-05-01 12:00:00"
        timestamp = datetime.strptime(observationTimeUtc, "%Y-%m-%d %H:%M:%S").isoformat() + "Z"

        fields = {
            "airTemperature": float(measurement.get("airTemperature")) if measurement.get("airTemperature") is not None else None,
            "feelsLikeTemperature": float(measurement.get("feelsLikeTemperature")) if measurement.get("feelsLikeTemperature") is not None else None,
            "windSpeed": float(measurement.get("windSpeed")) if measurement.get("windSpeed") is not None else None,
            "windDirection": float(measurement.get("windDirection")) if measurement.get("windDirection") is not None else None,
            "cloudCover": float(measurement.get("cloudCover")) if measurement.get("cloudCover") is not None else None,
            "seaLevelPressure": float(measurement.get("seaLevelPressure")) if measurement.get("seaLevelPressure") is not None else None,
            "relativeHumidity": float(measurement.get("relativeHumidity")) if measurement.get("relativeHumidity") is not None else None,
            "precipitation": float(measurement.get("precipitation")) if measurement.get("precipitation") is not None else None,
            "conditionCode": str(measurement.get("conditionCode")) if measurement.get("conditionCode") is not None else None,
        }
        # Remove None values
        fields = {k: v for k, v in fields.items() if v is not None}

        json_body.append({
            "measurement": "weather",
            "tags": {
                "station": stationCode
            },
            "time": timestamp,
            "fields": fields
        })

    client.write_points(json_body)

def main():
    print(f"[{datetime.now()}] Pushing data to InfluxDB.")
    weather_data = getWeatherData(STATION_ID)
    if weather_data:
        pushDataToInfluxDB(weather_data["station"]["code"], weather_data["observations"])
    else:
        print(f"[{datetime.now()}] No weather data returned.")

if __name__ == "__main__":
    main()

    if SCHEDULER_INTERVAL > 0:
        schedule.every(int(SCHEDULER_INTERVAL)).minutes.do(main)

        print(f"[{datetime.now()}] Starting scheduler. Interval: {SCHEDULER_INTERVAL} minutes")
        while True:
            schedule.run_pending()
            time.sleep(1)

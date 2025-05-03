# MeteoLT-InfluxDBv1

🇬🇧 Weather data importer from MeteoLT to InfluxDB v1.1+

🇱🇹 Meteorologinių duomenų nusiurbėjas iš MeteoLT į InfluxDB v1.1+

## Usage

Prerequisites:
- An active InfluxDB v1.1+ instance
- Python 3.11+ or Docker installed
- The desired station's ID

### Running thru CLI

```bash
# Install Prerequisites:
pip install -r requirements.txt

# Set environment variables:
export STATION_ID=your_station_id
export INFLUXDB_HOST=your_host
export INFLUXDB_PORT=8086
export INFLUXDB_DATABASE=your_db
export INFLUXDB_USERNAME=your_user
export INFLUXDB_PASSWORD=your_pass

# Run the script:
python src/main.py
```

### Running in Docker

```bash
# Build the image:
docker build -t meteolt-influxdb .

# Start the container:
docker run --rm -d \
  -e STATION_ID=your_station_id \
  -e INFLUXDB_HOST=your_host \
  -e INFLUXDB_PORT=8086 \
  -e INFLUXDB_DATABASE=your_db \
  -e INFLUXDB_USERNAME=your_user \
  -e INFLUXDB_PASSWORD=your_pass \
  --name meteolt-exporter meteolt-influxdb

# Stop the container:
docker stop meteolt-exporter
```

You can set the `SCHEDULER_INTERVAL` environment variable to make the script run at a specific inteval.

## Environment Variables

| **Variable Name** | **Description** | **Type** | **Default Value** | **Example** |
|-|-|-|-|-|
| `STATION_ID` | Weather station ID. | String | | `STATION_ID=kauno-ams` |
| `SCHEDULER_INTERVAL` | The interval (in minutes) at which the script should run. | Integer | `0` (disabled by default) | `SCHEDULER_INTERVAL=60` (runs every 60 minutes) |
| `INFLUXDB_MEASUREMENT` | The name of the measurement (or data collection) in InfluxDB where the weather data will be stored. | String | `weather` | `INFLUXDB_MEASUREMENT=weather` |
| `INFLUXDB_HOST` | The hostname or IP address of the InfluxDB server. | String | `localhost` | `INFLUXDB_HOST=192.168.2.20` |
| `INFLUXDB_PORT` | The port number for the InfluxDB server. | Integer | `8086` | `INFLUXDB_PORT=8086` |
| `INFLUXDB_DATABASE`| The name of the InfluxDB database to use for storing the weather data. | String | | `INFLUXDB_DATABASE=influx` |
| `INFLUXDB_USERNAME`| The username used to authenticate to the InfluxDB server. | String | | `INFLUXDB_USERNAME=admin` |
| `INFLUXDB_PASSWORD`| The password used to authenticate to the InfluxDB server. | String | | `INFLUXDB_PASSWORD=admin` |

## F.A.Q

### How to get the station ID?

All of the station id's can be found by requesting ``https://api.meteo.lt/v1/stations``.

You will need the `code` value.

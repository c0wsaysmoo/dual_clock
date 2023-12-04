from datetime import datetime, timedelta
import requests as r
import pytz
import time
import json 

# Attempt to load config data
try:
    from config import TOMORROW_API_KEY
    from config import TEMPERATURE_UNITS

except (ModuleNotFoundError, NameError, ImportError):
    # If there's no config data
    TOMORROW_API_KEY = None
    TEMPERATURE_UNITS = "metric"

if TEMPERATURE_UNITS != "metric" and TEMPERATURE_UNITS != "imperial":
    TEMPERATURE_UNITS = "metric"

from config import TEMPERATURE_LOCATION

# Weather API
TOMORROW_API_URL = "https://api.tomorrow.io/v4/"




def grab_weather_data(delay=2):
    current_temp, current_humidity, wind_speed, wind_direction, wind_gust = None, None, None, None, None

    while True:
        try:
            request = r.get(
                f"{TOMORROW_API_URL}/weather/realtime",
                params={
                    "location": TEMPERATURE_LOCATION,
                    "units": TEMPERATURE_UNITS,
                    "apikey": TOMORROW_API_KEY
                }
            )
            request.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = request.json()["data"]["values"]
            
            current_temperature = data.get("temperature")
            current_humidity = data.get("humidity")
            wind_speed = data.get("windSpeed")
            wind_direction = data.get("windDirection")
            wind_gust = data.get("windGust")

            break  # If successful, exit the loop and return the weather data
        except r.exceptions.RequestException as e:
            print(f"Request failed. Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    return current_temperature, current_humidity, wind_speed, wind_direction, wind_gust
    
def grab_forecast(delay=2):
    while True:
        try:
            current_time = datetime.utcnow()
            end_time = current_time + timedelta(hours=1)  # Adjusted to 1 hour
            
            resp = r.post(
                f"{TOMORROW_API_URL}/timelines",
                headers={
                    "Accept-Encoding": "gzip",
                    "accept": "application/json",
                    "content-type": "application/json"
                },
                params={"apikey": TOMORROW_API_KEY}, 
                json={
                    "location": TEMPERATURE_LOCATION,
                    "units": TEMPERATURE_UNITS,
                    "fields": [
                        "precipitationProbability"
                    ],
                    "timesteps": [
                        "1h"
                    ],
                    "startTime": current_time.isoformat(),
                    "endTime": (current_time + timedelta(hours=1)).isoformat()
                }
            )    
            resp.raise_for_status()
            
            # Return the intervals directly
            return resp.json()["data"]["timelines"][0].get("intervals", [])
        except (r.exceptions.RequestException, KeyError) as e:
            print(f"Request failed. Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    
    return None

def grab_rain(delay=2):
    while True:
        try:
            current_time = datetime.utcnow()
            dt = current_time + timedelta(hours=6)
            
            resp = r.post(
                f"{TOMORROW_API_URL}/timelines",
                headers={
                    "Accept-Encoding": "gzip",
                    "accept": "application/json",
                    "content-type": "application/json"
                },
                params={"apikey": TOMORROW_API_KEY}, 
                json={
                    "location": TEMPERATURE_LOCATION,
                    "units": TEMPERATURE_UNITS,
                    "fields": [
                        "precipitationProbability"
                    ],
                    "timesteps": [
                        "1d"
                    ],
                    "startTime": dt.isoformat(),
                    "endTime": (dt + timedelta(days=int(1))).isoformat()
                }
            )    
            resp.raise_for_status()  # Fix the method name here
            
            # Print the raw JSON response for debugging
            #print("Raw JSON Response:")
            #print(json.dumps(resp.json(), indent=4))
            rain = resp.json()["data"]["timelines"][0]["intervals"]
            return rain
        except (r.exceptions.RequestException, KeyError) as e:
            print(f"Request failed. Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    
    return None
    
forecast_data = grab_forecast()
if forecast_data is not None:
    print("Precipitation Probabilities:")
    for probability in forecast_data:
        print(f"Probability: {probability['values']['precipitationProbability']}")
else:
    print("Failed to retrieve forecast.")

rain_data = grab_rain()
if rain_data is not None:
    print("Rain Probabilities:")
    for probability in rain_data:
        print(f"Rain: {probability['values']['precipitationProbability']}")
else:
    print("Failed to retrieve forecast.")
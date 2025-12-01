import json
import boto3
import urllib.request
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
S3_BUCKET = "weather-apibucket"
OWM_API_KEY = "629c766ce6b56703b85da1323a1b442b"
CITY = "Sherbrooke"
UNITS = "metric"

# AWS S3 client
s3 = boto3.client("s3")

def fetch_weather():
    """Fetch weather forecast from OpenWeather."""
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={OWM_API_KEY}&units={UNITS}"
    response = urllib.request.urlopen(url)
    forecast = json.loads(response.read().decode())
    return forecast


def save_to_s3(data):
    """Upload JSON data to S3 with timestamped filename."""
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    key = f"weather_data/{timestamp}.json"

    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json"
    )

    return key


def main():
    print("Fetching weather data...")
    weather = fetch_weather()

    print("Uploading to S3...")
    file_key = save_to_s3(weather)

    print(f"✔ Upload complete: {file_key}")


if __name__ == "__main__":
    main()

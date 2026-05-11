import requests
import pandas as pd

# Cities with coordinates
cities = {
    "Mumbai": (19.07, 72.87),
    "Pune": (18.52, 73.85),
    "Delhi": (28.61, 77.21),
    "Bangalore": (12.97, 77.59),
    "Chennai": (13.08, 80.27),
    "Kolkata": (22.57, 88.36),
    "Hyderabad": (17.38, 78.48),
    "Jaipur": (26.91, 75.79)
}

URL = "https://api.open-meteo.com/v1/forecast"

rows = []

for city, (lat, lon) in cities.items():
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }

        r = requests.get(URL, params=params, timeout=10)
        r.raise_for_status()

        data = r.json()["current_weather"]

        rows.append({
            "city": city,
            "temperature": data["temperature"],
            "wind_speed": data["windspeed"],
            "wind_direction": data["winddirection"]
        })

    except Exception as e:
        print(f"Error for {city}: {e}")

# Convert to DataFrame
df = pd.DataFrame(rows)

# Clean data
df = df.dropna().drop_duplicates()

# Add extra column
df["feels_like"] = df["temperature"] - 2

# Save CSV
df.to_csv("weather_day7.csv", index=False)

print(" CSV saved!")

# Top 3 hottest cities
print("\n Top 3 hottest cities:")
print(df.nlargest(3, "temperature"))

# Extra analysis
print("\n Avg wind speed:", df["wind_speed"].mean())

# Max humidity placeholder (API doesn't give humidity here)
# But we simulate:
df["humidity"] = [60, 55, 70, 65, 75, 68, 72, 66]
print("\n Highest humidity city:")
print(df.loc[df["humidity"].idxmax()])
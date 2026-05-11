import requests
import json

API_KEY = "182baeabd5ec4d348bd131111262004"

def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url)

        data = response.json()

       
        if "error" in data:
            print(f"Error for {city}: {data['error']['message']}")
            return None

        temp = data["current"]["temp_c"]
        desc = data["current"]["condition"]["text"]

        result = {
            "city": city,
            "temperature": temp,
            "description": desc
        }

        print(f"{city}: {temp}°C, {desc}")

        
        with open(f"{city.lower()}_weather.json", "w") as f:
            json.dump(result, f, indent=4)

        return result

    except requests.exceptions.RequestException:
        print("Network error. Please check your internet.")
    except:
        print("Something went wrong.")



cities = ["Mumbai", "Pune", "Chennai"]

for c in cities:
    get_weather(c)

get_weather("Bangalore")
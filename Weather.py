import requests
import json

def get_weather_data(api_key, city_name):
    """Fetches current weather data for a given city using OpenWeatherMap API with error handling."""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"

    try:
        response = requests.get(complete_url)
        response.raise_for_status() 
        data = response.json()

        if data["cod"] == 200: 
            if "main" in data and "weather" in data and len(data["weather"]) > 0:
                main_data = data["main"]
                weather_data = data["weather"][0]
                return {
                    "city": data["name"],
                    "temperature": main_data["temp"],
                    "description": weather_data["description"].capitalize(),
                    "humidity": main_data["humidity"]
                }
            else:
                print(f"Error: Unexpected data format for {city_name}")
                return None
        elif data["cod"] == "404":
            print(f"Error: City '{city_name}' not found")
            return None
        else:
            print(f"Error: API returned code {data['cod']} for {city_name}: {data.get('message', 'No message')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: Network issue for {city_name}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON response for {city_name}: {e}")
        return None
    except KeyError as e:
        print(f"Error: Missing key '{e}' in API response for {city_name}")
        return None

def display_weather(city_weather):
    """Displays the weather information for a single city."""
    if city_weather:
        print(f"Weather in {city_weather['city']}:")
        print(f"  Temperature: {city_weather['temperature']} °C")
        print(f"  Description: {city_weather['description']}")
        print(f"  Humidity: {city_weather['humidity']}%")
    else:
        print("Weather data not available.")

if __name__ == "__main__":
    api_key ="2fa5e00d80d6b26d1c29624dbca6d124"
    cities_input = input("Enter a list of Indian city names (india): ")
    city_list = [city.strip() for city in cities_input.split(',')]

    for city in city_list:
        weather_info = get_weather_data(api_key, city)
        print(f"\n--- {city.capitalize()} ---")
        display_weather(weather_info)
        print("-" * (6 + len(city)))
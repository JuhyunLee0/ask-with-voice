import os, requests
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv('AZURE_MAPS_KEY')

# Azure Maps API setup: Convert city to lat/long
def get_lat_long(api_key, city_name):
    url = f"https://atlas.microsoft.com/search/address/json?api-version=1.0&query={city_name}&subscription-key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            latitude = data["results"][0]["position"]["lat"]
            longitude = data["results"][0]["position"]["lon"]
            return latitude, longitude
        else:
            return None, None
    else:
        return None, None

# Function to get weather data from Azure Maps API
def get_weather_data(api_key, latitude, longitude):
    
    if not api_key:
        return "Azure Maps API key not found."

    # Endpoint for Azure Maps Weather (you can adjust it based on the API you use)
    url = f"https://atlas.microsoft.com/weather/currentConditions/json?api-version=1.1&query={latitude},{longitude}&subscription-key={api_key}"

    headers = {
        'Ocp-Apim-Subscription-Key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        weather_data = response.json()

        return weather_data
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    
# print(get_weather("47.641268,-122.125679"))

# Format weather response
def format_weather_response(weather_data):
    
    weather_description = weather_data["results"][0]
    temperature = weather_description["temperature"]["value"]
    conditions = weather_description["phrase"]
    
    final_msg = f"The weather is {conditions} with a temperature of {temperature} °C degrees."
    return final_msg

# Main function to integrate Azure Maps and OpenAI
def get_weather_response(city_name):
    
    # Step 1: Convert city name to lat/long
    latitude, longitude = get_lat_long(api_key, city_name)
    
    if latitude and longitude:

        # Step 2: Get weather data from Azure Maps
        weather_data = get_weather_data(api_key, latitude, longitude)
        
        if weather_data:
            # Step 3: Use Azure OpenAI to generate a user-friendly response
            response = format_weather_response(weather_data)
            return response
        else:
            return "Sorry, I couldn't retrieve the weather information."
    else:
        return "Sorry, I couldn't find the location for the city you entered."

# Example usage:
city_name = "New York"
response = get_weather_response(city_name)
print(response)
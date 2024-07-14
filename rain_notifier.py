import requests
import random

# Webhook URL copied from Discord
webhook_url = 'https://discord.com/api/webhooks/1251880694871883867/Jjh7JNMEfiGDLr8c4tazFdBC5eUKPzgMJ4VUptncR9v8c5NXnEDYaPNXQxW0c976of_8'

# OpenWeatherMap endpoint and key
api_key = 'f7aa3ef91ada794dd4718a17cf150744'
endpoint = 'http://api.openweathermap.org/data/2.5/weather'

# List of random cities (You can expand this list)
random_cities = [
    'Tokyo,JP', 'Paris,FR', 'London,GB', 'Berlin,DE', 'Beijing,CN',
    'Sydney,AU', 'Moscow,RU', 'Cairo,EG', 'Mumbai,IN', 'Rio de Janeiro,BR',
    'New York,US', 'Los Angeles,US', 'Chicago,US', 'Houston,US', 'Phoenix,US',
    'San Antonio,US', 'San Diego,US', 'Dallas,US', 'San Jose,US', 'Austin,US',
    'Rotorua,NZ', 'Banff,CA', 'Hobart,AU', 'Queenstown,NZ', 'Inverness,UK',
    'Reykjavik,IS', 'Cusco,PE', 'Sedona,US', 'Bozeman,US', 'Flagstaff,US',
    'Moab,US', 'Aspen,US', 'Vail,US', 'St. Moritz,CH', 'Garmisch-Partenkirchen,DE',
    'Chamonix,FR', 'Zermatt,CH', 'Whistler,CA', 'Davos,CH', 'Wanaka,NZ', 'Asuncion,PY'
]

# Function to check weather in a specific location
def check_weather(location):
    params = {
        'q': location,
        'appid': api_key,
        'units': 'imperial'  # Use 'metric' for Celsius
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        print(f"Successfully fetched weather data for {location}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {location}: {e}")
        return None

# Function to send a message to Discord
def send_discord_message(content):
    headers = {
        "Content-Type": "application/json"
    }
    message = {
        "content": content,
        "username": "Weather Bot"
    }
    try:
        response = requests.post(webhook_url, json=message, headers=headers)
        response.raise_for_status()
        print(f"Successfully sent notification: {content}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {e}")

# Function to test Discord webhook
def test_discord_webhook():
    send_discord_message("Standby For Raindar Report...")

# Call the test function
test_discord_webhook()

# Locations in the eastern US to monitor
locations = ['Albany,NY,US', 'Indianapolis,IN,US', 'Ocala,FL,US', 'Miami,FL,US']

print("Starting script...")

# List to store individual location reports
location_reports = []

# Messages for different weather conditions
rain_messages = [
    "It's raining really hard in {}.",
    "Sheesh, it's a wet one in {}.",
    "Look out, it's raining hard in {}.",
    "Looks like {} is getting soaked with rain.",
    "{} has heavy rain."
]

no_rain_messages = [
    "No rain in {}.",
    "It's dry in {}.",
    "No precipitation in {}.",
]

# Check weather in each location and store the report
for location in locations:
    print(f"Checking weather for {location}...")
    weather_data = check_weather(location)
    if weather_data:
        print(weather_data)  # Print the weather data for debugging purposes
        weather_condition = weather_data.get('weather', [{}])[0].get('main', '').lower()
        rain_amount = weather_data.get('rain', {}).get('1h', 0)  # Get the rainfall amount in the last hour if available
        print(f"Weather condition in {location}: {weather_condition}, Rain amount: {rain_amount} mm")
        
        if 'rain' in weather_condition:
            report = random.choice(rain_messages).format(location)
        else:
            report = random.choice(no_rain_messages).format(location)
        
        location_reports.append(report)
    else:
        print(f"Failed to retrieve weather data for {location}.")

# List to store cities where it is raining
raining_cities = []

# Check weather for all random cities and find those where it is raining
for city in random_cities:
    weather_data = check_weather(city)
    if weather_data:
        weather_condition = weather_data.get('weather', [{}])[0].get('main', '').lower()
        if 'rain' in weather_condition:
            raining_cities.append(city)

# Select a random city from the raining cities list
random_city_report = ""
if raining_cities:
    random_city = random.choice(raining_cities)
    random_city_weather = check_weather(random_city)
    if random_city_weather:
        weather_condition = random_city_weather.get('weather', [{}])[0].get('main', '').lower()
        rain_amount = random_city_weather.get('rain', {}).get('1h', 0)
        print(f"Weather condition in {random_city}: {weather_condition}, Rain amount: {rain_amount} mm")
        
        if 'rain' in weather_condition:
            random_city_report = random.choice(rain_messages).format(random_city)
else:
    random_city_report = "No more rain."

# Create a final message to send to Discord
final_message = "\n".join(location_reports)
if random_city_report:
    final_message += f"\n{random_city_report}"

# Send the final message to Discord
send_discord_message(final_message)

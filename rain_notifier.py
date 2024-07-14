import requests

# Webhook URL copied from Discord
webhook_url = 'https://discord.com/api/webhooks/1251880694871883867/Jjh7JNMEfiGDLr8c4tazFdBC5eUKPzgMJ4VUptncR9v8c5NXnEDYaPNXQxW0c976of_8'

# OpenWeatherMap endpoint and key
api_key = 'f7aa3ef91ada794dd4718a17cf150744'
endpoint = 'http://api.openweathermap.org/data/2.5/weather'

# Function to check weather in a specific location
def check_weather(location):
    params = {
        'q': location,
        'appid': api_key,
        'units': 'imperial'  # Use 'metric' for Celsius
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather data: {response.status_code}, {response.text}")
        return None

# Locations in the eastern US to monitor
locations = ['Albany,NY,US', 'Indianapolis,IN,US', 'Ocala,FL,US', 'Miami,FL,US']

print("Starting script...")

# Check weather in each location and send a notification if it's raining
for location in locations:
    print(f"Checking weather for {location}...")
    weather_data = check_weather(location)
    if weather_data:
        print(weather_data)  # Print the weather data for debugging purposes
        weather_condition = weather_data.get('weather', [{}])[0].get('main', '').lower()
        print(f"Weather condition in {location}: {weather_condition}")
        if 'rain' in weather_condition:
            message = {
                "content": f"It's raining in {location}!",
                "username": "Rain Notifier"
            }
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(webhook_url, json=message, headers=headers)
            if response.status_code == 204:
                print(f'Successfully sent notification for {location}.')
            else:
                print(f'Error sending notification for {location}: {response.status_code}, {response.text}')
        else:
            print(f"No rain in {location}.")
    else:
        print(f"Failed to retrieve weather data for {location}.")

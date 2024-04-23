import requests
import datetime
import streamlit as st




# Function to get weather data
def get_weather(city):
    api_key = "5609e5c95ae59033e36538f65e15b9da"
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    weather = weather_data.json()['weather'][0]['main']
    temp = round(weather_data.json()['main']['temp'])
    temp_celsius = round(temp - 273,15)  # Convert temperature from Fahrenheit to Celsius
    return weather, temp_celsius

# Streamlit app
def main():
    st.title("Weather App")
    city = st.text_input("Enter City")
    if st.button("Get Weather"):
        weather, temp = get_weather(city)
        st.write(f"The weather in {city} is {weather} with a temperature of {temp}°C")

if __name__ == "__main__":
    main()
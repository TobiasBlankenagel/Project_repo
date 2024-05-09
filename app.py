#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 15:02:55 2024

@author: nicolasviglietti
"""

import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Set Streamlit page configuration
st.set_page_config(page_title="Weather Forecast App", layout="wide")

# Setting a custom theme for the app
st.markdown("""
<style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .text-font {
        font-size:20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Weather Forecast Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="text-font">Find out the weather forecast by entering a city name.</p>', unsafe_allow_html=True)

city = st.text_input("Enter a city", value="Berlin", key="city")

def fetch_weather_data(city, api_key="bf5fb212639617ff3234076f22c65c87"):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    forecast_items = data['list']
    dates = []
    temperatures = []
    precipitations = []
    
    for item in forecast_items:
        date = pd.to_datetime(item['dt_txt'])
        temperature = item['main']['temp']
        precipitation = item.get('rain', {}).get('3h', 0)
        
        dates.append(date)
        temperatures.append(temperature)
        precipitations.append(precipitation)
    
    df = pd.DataFrame({
        "Date": dates,
        "Temperature": temperatures,
        "Precipitation": precipitations
    })
    
    return df

def plot_weather_data(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature (°C)', color=color)
    ax1.plot(df['Date'], df['Temperature'], color=color, marker='o', linestyle='-')
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Precipitation (mm)', color=color)
    ax2.bar(df['Date'], df['Precipitation'], color=color, alpha=0.6, width=0.02)
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Setting lower x-axis for specific hours
    specific_hours = [date for date in df['Date'] if date.hour in [0, 4, 8, 12, 16, 20]]
    ax1.set_xticks(specific_hours)
    ax1.set_xticklabels([date.strftime('%H:%M') for date in specific_hours], rotation=45)
    
    # Creating a secondary x-axis at the top for the date
    ax3 = ax1.twiny()
    ax3.set_xlim(ax1.get_xlim())
    ax3.set_xticks(ax1.get_xticks())
    ax3.set_xticklabels([date.strftime('%Y-%m-%d') for date in specific_hours], rotation=45)
    ax3.set_xlabel('Date')
    
    plt.grid(True)
    plt.title(f"Weather Forecast for {city.title()}", fontsize=16)
    fig.tight_layout()
    st.pyplot(fig)

if city:
    try:
        weather_data = fetch_weather_data(city)
        plot_weather_data(weather_data)
    except Exception as e:
        st.error(f"An error occurred: {e}")
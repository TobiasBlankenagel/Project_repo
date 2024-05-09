import streamlit as st
import requests

def load_css():
    css = """
    <style>
        body {
            background-color: #f0f2f5;
            font-family: 'Arial', sans-serif;
        }
        h1 {
            color: #4a4e69;
            text-align: center;
        }
        .stTextInput>label, .stButton>button {
            color: #4a4e69;
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 2px solid #4a4e69;
            padding: 10px;
        }
        .stButton>button {
            border-radius: 20px;
            border: none;
            background-color: #4a4e69;
            color: white;
            padding: 10px 24px;
            font-size: 16px;
            margin-top: 10px;
            width: 100%;
        }
        .report {
            border-radius: 10px;
            background-color: #ffffff;
            padding: 20px;
            box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
            margin-top: 10px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def fetch_location_data(city):
    """ Holt die Koordinaten eines Ortes für die Wetterkarte. """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": "YOUR_API_KEY",  # Ersetzen Sie 'YOUR_API_KEY' mit Ihrem eigenen API-Schlüssel
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['coord']['lat'], data['coord']['lon']
    else:
        return None, None

def main():
    load_css()  # Stildefinitionen laden
    st.title('Wetterabfrage und -karte')

    city = st.text_input("Gib einen Ort ein:", "")
    if st.button('Wetter abrufen'):
        lat, lon = fetch_location_data(city)
        if lat and lon:
            map_url = f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer=temperature&lat={lat}&lon={lon}&zoom=8"
            st.components.v1.iframe(map_url, width=700, height=500)
        else:
            st.error("Keine Wetterdaten verfügbar oder der Ort wurde nicht gefunden.")

if __name__ == "__main__":
    main()

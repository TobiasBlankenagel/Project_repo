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

def main():
    load_css()  # Stildefinitionen laden
    st.title('Wetterabfrage')

    city = st.text_input("Gib einen Ort ein:", "")

    if st.button('Wetter abrufen'):
        weather = fetch_weather(city)
        if weather:
            display_weather(weather)
        else:
            st.error("Keine Wetterdaten verfügbar.")

def fetch_weather(city):
    # Simulierter API-Aufruf (ersetzen Sie diesen durch tatsächliche API-Aufrufe)
    if city.lower() == "berlin":
        return {
            "temperatur": "18°C",
            "beschreibung": "Teilweise bewölkt",
            "wind": "10 km/h"
        }
    return None

def display_weather(weather):
    st.markdown(f"""
        <div class='report'>
            <h2>Wetterbericht</h2>
            <p><b>Temperatur:</b> {weather['temperatur']}</p>
            <p><b>Beschreibung:</b> {weather['beschreibung']}</p>
            <p><b>Wind:</b> {weather['wind']}</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

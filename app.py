









import streamlit as st
import requests
import os


# Die Funktion, die die API aufruft
def get_flight_data(from_airport, to_airport):
    url = 'https://skyscanner80.p.rapidapi.com/api/v1/checkServer'  # URL aktualisieren
    headers = {
	"X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
	"X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }

    
    try:
        response = requests.get(url, headers=headers)
        return response.json()  # Antwort als JSON zurückgeben
    except requests.exceptions.RequestException as e:
        return str(e)  # Fehler als String zurückgeben

# Streamlit-Seite konfigurieren
st.title('Flugsuche')

# Eingabefelder für Flughäfen
from_airport = st.text_input('Abflughafen', '')
to_airport = st.text_input('Zielflughafen', '')

# Suchknopf
if st.button('Suche günstige Flüge'):
    if from_airport and to_airport:
        # API aufrufen und Daten holen
        result = get_flight_data(from_airport, to_airport)
        st.write(result)
    else:
        st.error('Bitte geben Sie sowohl den Abflug- als auch den Zielflughafen an.')


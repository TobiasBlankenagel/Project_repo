import streamlit as st
import requests
from datetime import date

# Autocomplete Suchleiste für Nutzer
def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "Hier-deinen-eigenen-RapidAPI-Key-einfügen",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Verarbeitet und speichert Autocomplete-Daten, prüft auf Flughafentyp
def process_and_display_autocomplete_data(data):
    if data and 'data' in data:
        st.write("Gefundene Flughäfen:")
        airports = []
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                sky_id = item['navigation']['relevantFlightParams']['skyId']
                name = item['presentation']['title']
                subtitle = item['presentation']['subtitle']
                st.write(f"{name} ({sky_id}) - {subtitle}")
                airports.append({'sky_id': sky_id, 'name': name})
        if airports:
            st.session_state['airports'] = airports
        else:
            st.write("Keine Flughäfen gefunden.")
    else:
        st.error("Keine Daten gefunden oder unerwartete Antwortstruktur.")

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Flughafen Auto-Complete Suche und Fluginformationen')

    query = st.text_input('Geben Sie einen Standort ein', '')
    if st.button("Suche"):
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            process_and_display_autocomplete_data(autocomplete_data)
        else:
            st.write("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()


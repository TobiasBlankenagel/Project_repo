import streamlit as st
import requests
from datetime import date

# Autocomplete Suchleiste für Nutzer
def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Verarbeitet Daten und sammelt Flughafeninformationen
def process_and_collect_locations(data):
    location_info = []
    if data and 'data' in data:
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                city_country = f"{item['presentation']['title']} ({item['presentation']['subtitle']})"
                iata_code = item['navigation']['relevantFlightParams']['skyId']
                location_info.append((city_country, iata_code))
    return location_info

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen')

    query = st.text_input('Geben Sie einen Standort ein', '')
    if query:
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            location_info = process_and_collect_locations(autocomplete_data)
            if location_info:
                # Erstellt eine Auswahlliste mit Flughafenname und speichert den IATA-Code
                options = [info[0] for info in location_info]
                index_selected = st.selectbox("Wählen Sie einen Flughafen:", options, format_func=lambda x: x)
                if st.button("Auswahl bestätigen"):
                    # Findet den IATA-Code für den ausgewählten Flughafen
                    iata_code = location_info[options.index(index_selected)][1]
                    st.write(f"Sie haben {index_selected} ausgewählt. IATA-Code: {iata_code}")
                    # Optional: Speichern des IATA-Codes für weitere Verwendung
                    st.session_state['iata_code'] = iata_code
            else:
                st.write("Keine Flughäfen gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

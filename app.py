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

# Speichert die gefundenen Airports ab und zeigt nur die EntityIDs an
def process_and_collect_locations(data):
    locations = []
    if data and 'data' in data:
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                city_country = f"{item['presentation']['title']} ({item['presentation']['subtitle']})"
                locations.append(city_country)
        return locations
    return []

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen')

    query = st.text_input('Geben Sie einen Standort ein', '')
    if query:
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            locations = process_and_collect_locations(autocomplete_data)
            if locations:
                location_selected = st.selectbox("Wählen Sie einen Flughafen:", locations)
                if st.button("Auswahl bestätigen"):
                    st.write(f"Sie haben {location_selected} ausgewählt.")
            else:
                st.write("Keine Flughäfen gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

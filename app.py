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
def process_and_display_entity_ids(data):
    if data and 'data' in data:
        st.write("Gefundene Flughäfen und deren Entity IDs:")
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                IATA_id = item['navigation']['relevantFlightParams']['skyId']
                name = item['presentation']['title']
                subtitle = item['presentation']['subtitle']
                st.write(f"{name} - {subtitle}: IATA = {IATA_id}")
    else:
        st.error("Keine Daten gefunden oder unerwartete Antwortstruktur.")

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen')

    with st.form("search_form"):
        query = st.text_input('Geben Sie einen Standort ein', '')
        submitted = st.form_submit_button("Suche")

        if submitted and query:
            autocomplete_data = fetch_autocomplete_data(query)
            if autocomplete_data:
                process_and_display_entity_ids(autocomplete_data)
            else:
                st.write("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

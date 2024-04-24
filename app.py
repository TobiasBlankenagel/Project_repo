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
        countries = set()
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                country = item['presentation']['subtitle']
                countries.add(country)

        if len(countries) > 1:
            country_selected = st.selectbox("Wählen Sie ein Land:", list(countries))
            display_airports_by_country(data, country_selected)
        elif countries:
            display_airports_by_country(data, list(countries)[0])
    else:
        st.error("Keine Daten gefunden oder unerwartete Antwortstruktur.")

# Zeigt die Flughäfen an, die zu dem ausgewählten Land gehören
def display_airports_by_country(data, country_selected):
    st.write(f"Gefundene Flughäfen in {country_selected} und deren IATA-Codes:")
    iata_codes = []
    for item in data['data']:
        if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
            subtitle = item['presentation']['subtitle']
            if subtitle == country_selected:
                IATA_id = item['navigation']['relevantFlightParams']['skyId']
                name = item['presentation']['title']
                st.write(f"{name}: IATA = {IATA_id}")
                iata_codes.append(IATA_id)
    st.session_state['iata_codes'] = iata_codes

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

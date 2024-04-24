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
def process_and_collect_countries(data):
    if data and 'data' in data:
        countries = set()
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                country = item['presentation']['subtitle']
                countries.add(country)
        return list(countries)
    return []

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
    if iata_codes:
        st.session_state['iata_codes'] = iata_codes

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen')

    query = st.text_input('Geben Sie einen Standort ein', '')
    if st.button("Suche"):
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            countries = process_and_collect_countries(autocomplete_data)
            if countries:
                st.session_state['autocomplete_data'] = autocomplete_data
                country_selected = st.selectbox("Wählen Sie ein Land:", countries)
                st.session_state['country_selected'] = country_selected
                if st.button("Land bestätigen"):
                    display_airports_by_country(st.session_state['autocomplete_data'], st.session_state['country_selected'])
            else:
                st.write("Keine Flughäfen gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

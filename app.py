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

# Sammelt Flughafeninformationen nach Land
def process_and_collect_locations(data, country_choice):
    location_info = []
    if data and 'data' in data:
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT' and item['presentation']['subtitle'].endswith(country_choice):
                city_country = f"{item['presentation']['title']} ({item['presentation']['subtitle']})"
                iata_code = item['navigation']['relevantFlightParams']['skyId']
                location_info.append((city_country, iata_code))
    return location_info

# Abfrage der Flugdaten für ein bestimmtes Datum und mehrere IATA-Codes
def fetch_flights(departure_date, iata_codes):
    flights_data = []
    url = "https://flight-info-api.p.rapidapi.com/schedules"
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com"
    }
    for iata_code in iata_codes:
        querystring = {
            "version": "v2",
            "DepartureDateTime": departure_date,
            "DepartureAirport": iata_code,
            "CodeType": "IATA",
            "ServiceType": "Passenger"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json().get('data', [])
            flights_data.extend(data)
    return flights_data

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen und Flugdatenabfrage')

    query = st.text_input('Geben Sie einen Standort ein, z.B. London', '')
    country_choice = st.text_input('Geben Sie das Land ein, z.B. United Kingdom', '')
    departure_date = st.date_input('Wählen Sie ein Abflugdatum', min_value=date.today())

    if st.button("Suche starten"):
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            location_info = process_and_collect_locations(autocomplete_data, country_choice)
            if location_info:
                iata_codes = [info[1] for info in location_info]
                flights_data = fetch_flights(departure_date.isoformat(), iata_codes)
                if flights_data:
                    st.write("Internationale Flüge gefunden:")
                    st.json(flights_data)
                else:
                    st.write("Keine internationalen Flüge gefunden.")
            else:
                st.write("Keine Flughäfen im gewählten Land gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

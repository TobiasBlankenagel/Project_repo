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

# Extrahiert Länder aus den Autocomplete-Daten
def extract_countries(data):
    countries = set()
    if data and 'data' in data:
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                country = item['presentation']['subtitle'].split(",")[-1].strip()
                countries.add(country)
    return sorted(list(countries))

# Sammelt Flughafeninformationen nach Land
def process_and_collect_locations(data, country_choice):
    location_info = []
    if data and 'data' in data:
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT' and item['presentation']['subtitle'].endswith(country_choice):
                city_country = f"{item['presentation']['title']} ({item['presentation']['subtitle']})"
                iata_code = item['navigation']['relevantFlightParams']['skyId']
                location_info.append((city_country, iata_code, item['presentation']['subtitle']))
    return location_info

# Abfrage der Flugdaten für ein bestimmtes Datum und mehrere IATA-Codes
def fetch_flights(departure_date, locations):
    flights_data = []
    url = "https://flight-info-api.p.rapidapi.com/schedules"
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com"
    }
    for city_country, iata_code, departure_country in locations:
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
            # Filter out domestic flights
            international_flights = [flight for flight in data if flight['arrival']['country']['code'] != departure_country]
            flights_data.extend(international_flights)
    return flights_data

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen und Flugdatenabfrage')

    query = st.text_input('Geben Sie einen Standort ein, z.B. London', '')
    if query:
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            countries = extract_countries(autocomplete_data)
            country_choice = st.selectbox('Wählen Sie ein Land aus', countries)
            departure_date = st.date_input('Wählen Sie ein Abflugdatum', min_value=date.today())
            if st.button("Suche starten"):
                location_info = process_and_collect_locations(autocomplete_data, country_choice)
                if location_info:
                    flights_data = fetch_flights(departure_date.isoformat(), location_info)
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

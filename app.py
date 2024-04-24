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

# Abfrage der Flugdaten für ein bestimmtes Datum und einen IATA-Code
def fetch_flights(departure_date, iata_code):
    url = "https://flight-info-api.p.rapidapi.com/schedules"
    querystring = {
        "version": "v2",
        "DepartureDateTime": departure_date,
        "DepartureAirport": iata_code,
        "CodeType": "IATA",
        "ServiceType": "Passenger"
    }
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        return filter_international_flights(data)
    else:
        return {"error": "Unable to fetch data", "status_code": response.status_code}

# Filtert internationale Flüge basierend auf dem Country-Code
def filter_international_flights(flight_data):
    if 'data' in flight_data and flight_data['data']:
        departure_country_code = flight_data['data'][0]['departure']['country']['code']
        international_flights = [flight for flight in flight_data['data']
                                 if flight['arrival']['country']['code'] != departure_country_code]
        return {"data": international_flights}
    return {"data": []}

# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen und Flugdatenabfrage')

    query = st.text_input('Geben Sie einen Standort ein', '')
    departure_date = st.date_input('Wählen Sie ein Abflugdatum', min_value=date.today())

    if query:
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            location_info = process_and_collect_locations(autocomplete_data)
            if location_info:
                options = [info[0] for info in location_info]
                index_selected = st.selectbox("Wählen Sie einen Flughafen:", options, format_func=lambda x: x)
                if st.button("Auswahl bestätigen"):
                    iata_code = location_info[options.index(index_selected)][1]
                    st.write(f"Sie haben {index_selected} ausgewählt. IATA-Code: {iata_code}")
                    flights_data = fetch_flights(departure_date.isoformat(), iata_code)
                    if 'data' in flights_data:
                        st.json(flights_data)
                    else:
                        st.write("Keine internationalen Flüge gefunden.")
            else:
                st.write("Keine Flughäfen gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

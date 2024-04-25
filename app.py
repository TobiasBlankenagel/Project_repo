import streamlit as st
import requests
from datetime import date

# Autocomplete Suchleiste für Nutzer
def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "DE", "locale": "de-DE"}
    headers = {
        "X-RapidAPI-Key": "1ebd07a20dmsh3d8c30c0e64a87ep15d844jsn48cdaa310b4a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Fetch airport details like latitude and longitude using IATA code
def get_airport_details(iata_code):
    url = f"https://aviation-reference-data.p.rapidapi.com/airports/{iata_code}"
    headers = {
        "X-RapidAPI-Key": "3079417e42mshe0aa2e580bcff7bp13da24jsn11f2ff015d49",
        "X-RapidAPI-Host": "aviation-reference-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Sammelt und wählt das Land mit den meisten Flughäfen automatisch aus
def get_most_frequent_country(autocomplete_data):
    country_count = {}
    for item in autocomplete_data.get('data', []):
        if item['navigation']['entityType'] == 'AIRPORT':
            country = item['presentation']['subtitle']
            if country in country_count:
                country_count[country] += 1
            else:
                country_count[country] = 1
    # Wählt das Land mit den meisten Flughäfen
    return max(country_count, key=country_count.get) if country_count else None

# Abfrage der Flugdaten für ein bestimmtes Datum und mehrere IATA-Codes
def fetch_flights(departure_date, locations):
    flights_data = []
    departure_times = set()  # Set zum Speichern der Abflugzeiten
    url = "https://flight-info-api.p.rapidapi.com/schedules"
    headers = {
        "X-RapidAPI-Key": "1ebd07a20dmsh3d8c30c0e64a87ep15d844jsn48cdaa310b4a",
        "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com"
    }

    for iata_code in locations:
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
            for flight in data:
                departure_time_utc = flight['departure']['time']['utc']
                if departure_time_utc not in departure_times:  # Überprüfen, ob die Zeit schon vorhanden ist
                    if flight['arrival']['country']['code'] != flight['departure']['country']['code']:
                        flights_data.append(flight)
                        departure_times.add(departure_time_utc)  # Zeit zur Menge hinzufügen

    return flights_data


def main():
    st.title('Auto-Complete Suche für Flughäfen und Flugdatenabfrage')

    col1, col2 = st.columns(2)
    with col1:
        query = st.text_input('Geben Sie einen Standort ein, z.B. London', '')
    with col2:
        departure_date = st.date_input('Wählen Sie ein Abflugdatum', min_value=date.today())

    if st.button("Suche starten") and query:
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            country_choice = get_most_frequent_country(autocomplete_data)
            location_info = []
            for item in autocomplete_data.get('data', []):
                # Überprüfe, ob das aktuelle Element ein Flughafen ist
                if item['navigation']['entityType'] == 'AIRPORT':
                    # Überprüfe, ob der Untertitel des Items mit der Länderauswahl endet
                    if item['presentation']['subtitle'] == country_choice:
                        # Hole die skyId und füge sie zur location_info Liste hinzu
                        sky_id = item['navigation']['relevantFlightParams']['skyId']
                        location_info.append(sky_id)
            flights_data = fetch_flights(departure_date.isoformat(), location_info)
            if flights_data:
                st.write("Internationale Flüge gefunden:")
                st.json(flights_data)
            else:
                st.write("Keine internationalen Flüge gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

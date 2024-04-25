import streamlit as st
import requests
from datetime import date

# Autocomplete Suchleiste für Nutzer
import time

def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "DE", "locale": "de-DE"}
    headers = {
        "X-RapidAPI-Key": "89fa2cdc22mshef83525ac6af5ebp10c163jsnc8047ffa3882",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    time.sleep(1)  # Verzögerung, um weniger wie ein Bot zu wirken
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        if not data.get('status', True):  # Prüft den Status; Standardwert ist True für den Fall, dass 'status' nicht vorhanden ist
            st.error("Die API denkt, dass Sie ein Bot sind. Bitte versuchen Sie, die Anfrage zu wiederholen.")
            return None
        return data
    st.error("Fehler beim Abrufen der Daten. Statuscode: {}".format(response.status_code))
    return None


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
    seen_flights = set()  # Speichert Tuples aus Uhrzeit und Ziel-IATA-Code

    url = "https://flight-info-api.p.rapidapi.com/schedules"
    headers = {
        "X-RapidAPI-Key": "89fa2cdc22mshef83525ac6af5ebp10c163jsnc8047ffa3882",
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
                departure_time_local = flight['departure']['date']['local']
                arrival_iata = flight['arrival']['airport']['iata']
                flight_key = (departure_time_local, arrival_iata)
                flights_data.append(flight)



    return flights_data

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": "afe025cb2b8a2785c5837a3eaed7b62a",
        "units": "metric",
        "lang": "de"
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def filter_flights_by_temperature(flights_details, temp_min, temp_max):
    filtered_flights = []
    for flight in flights_details:
        temp = flight.get("Temperature (C)", None)  # Holt den Temperaturwert, Standard ist None
        # Überprüft, ob die Temperatur nicht None ist und ob sie innerhalb der gesetzten Grenzen liegt
        if temp is not None:  # Stellt sicher, dass temp einen gültigen Wert hat
            if (temp_min is None or temp >= temp_min) and (temp_max is None or temp <= temp_max):
                filtered_flights.append(flight)
    return filtered_flights

def display_flight_details(flight_id):
    # Diese Funktion könnte detaillierte Informationen zum ausgewählten Flug anzeigen
    st.write(f"Details für Flug {flight_id}")

def get_city_by_coordinates(lat, lon):
    url = "https://geocodeapi.p.rapidapi.com/GetLargestCities"
    # Erhöht den Bereich auf 30000 Meter, um die größte Stadt in der Nähe zu finden
    querystring = {"latitude": str(lat), "longitude": str(lon), "range": "30000"}
    headers = {
        "X-RapidAPI-Key": "89fa2cdc22mshef83525ac6af5ebp10c163jsnc8047ffa3882",
        "X-RapidAPI-Host": "geocodeapi.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        # Prüft, ob Daten vorhanden sind und gibt die Stadt aus dem ersten Eintrag zurück
        if data:
            # Angenommen, die Antwort enthält eine Liste von Städten, sortiert nach ihrer Größe
            largest_city = data[0].get('City', 'Unbekannte Stadt')
            return largest_city



def main():
    st.title('Suche dein Ferienerlebnis!')
    query = st.text_input('Gib einen Standort ein', '')
    departure_date = st.date_input('Wähl ein Abflugdatum', min_value=date.today())
    temp_min = st.number_input('Minimale Temperatur (°C) am Ziel', format="%d", step=1)
    temp_max = st.number_input('Maximale Temperatur (°C) am Ziel', format="%d", step=1)

    if st.button("Suche starten") and query:
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data is None:
            return
        if autocomplete_data:
            country_choice = get_most_frequent_country(autocomplete_data)
            location_info = [item['navigation']['relevantFlightParams']['skyId'] for item in autocomplete_data.get('data', []) if item['navigation']['entityType'] == 'AIRPORT' and item['presentation']['subtitle'] == country_choice]
            flights_data = fetch_flights(departure_date.isoformat(), location_info)
            airports_details = []
            for flight in flights_data:
                airport_info = get_airport_details(flight['arrival']['airport']['iata'])
                if airport_info:
                    city_name = get_city_by_coordinates(airport_info['latitude'], airport_info['longitude'])
                    weather_info = get_weather(airport_info['latitude'], airport_info['longitude'])
                    airports_details.append({
                        "Destination": city_name,
                        "IATA": flight['arrival']['airport']['iata'],
                        "Departure Time (local)": flight['departure']['time']['local'],
                        "Latitude": airport_info['latitude'],
                        "Longitude": airport_info['longitude'],
                        "Weather Condition": weather_info['weather'][0]['description'] if weather_info else "No data",
                        "Temperature (C)": weather_info['main']['temp'] if weather_info else "No data"
                    })

            filtered_flights = filter_flights_by_temperature(airports_details, temp_min if temp_min != 0 else None, temp_max if temp_max != 0 else None)
            if filtered_flights:
                st.write("Gefilterte Flüge gefunden:")
                for flight in filtered_flights:
                    with st.expander(f"Flug nach {flight['Destination']} (IATA: {flight['IATA']})"):
                        st.write(f"Abflugzeit (lokal): {flight['Departure Time (local)']}")
                        st.write(f"Latitude: {flight['Latitude']}, Longitude: {flight['Longitude']}")
                        st.write(f"Wetter: {flight['Weather Condition']} bei {flight['Temperature (C)']} °C")
                        if st.button("Mehr Details", key=flight['IATA']):
                            display_flight_details(flight['IATA'])
            else:
                st.write("Keine Flüge gefunden, die den Temperaturkriterien entsprechen.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

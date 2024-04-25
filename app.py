import streamlit as st
import requests
from datetime import date

# Autocomplete Suchleiste für Nutzer
import time

def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "DE", "locale": "de-DE"}
    headers = {
        "X-RapidAPI-Key": "1ebd07a20dmsh3d8c30c0e64a87ep15d844jsn48cdaa310b4a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    # Eine kurze Verzögerung einführen, um weniger bot-artig zu wirken
    time.sleep(1)  # Eine Sekunde warten
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
    st.write(country_count)
    return max(country_count, key=country_count.get) if country_count else None

# Abfrage der Flugdaten für ein bestimmtes Datum und mehrere IATA-Codes
def fetch_flights(departure_date, locations):
    flights_data = []
    seen_flights = set()  # Speichert Tuples aus Uhrzeit und Ziel-IATA-Code

    url = "https://flight-info-api.p.rapidapi.com/schedules"
    headers = {
        "X-RapidAPI-Key": "ffcf62515fmsh41b890b8371e503p1cda22jsn67c89bfef1c7",
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
                departure_time_utc = flight['departure']['date']['utc']
                arrival_iata = flight['arrival']['airport']['iata']
                flight_key = (departure_time_utc, arrival_iata)

                # Prüft nur, ob die gleiche Uhrzeit zum gleichen Zielort bereits gesehen wurde
                if flight_key not in seen_flights:
                    flights_data.append(flight)
                    seen_flights.add(flight_key)
                # Andernfalls, wenn es zur gleichen Zeit ist aber unterschiedliche Ziele hat, wird es auch hinzugefügt
                elif all(flight_key[0] != f[0] or flight_key[1] != f[1] for f in seen_flights):
                    flights_data.append(flight)

    return flights_data

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": "afe025cb2b8a2785c5837a3eaed7b62a",
        "units": "metric",  # Setzt die Temperatureinheit auf Celsius
        "lang": "de"  # Ergebnisse auf Deutsch
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        weather = response.json()
        temperature = weather['main']['temp']  # Temperatur in Celsius
        condition = weather['weather'][0]['description']  # Wetterbeschreibung
        return {"Temperature": temperature, "Condition": condition}
    return None


def main():
    st.title('Auto-Complete Suche für Flughäfen und Flugdatenabfrage')

    col1, col2 = st.columns(2)
    with col1:
        query = st.text_input('Geben Sie einen Standort ein, z.B. London', '')
    with col2:
        departure_date = st.date_input('Wählen Sie ein Abflugdatum', min_value=date.today())

    if st.button("Suche starten") and query:
        autocomplete_data = fetch_autocomplete_data(query)
        st.json(autocomplete_data)
        if autocomplete_data:
            country_choice = get_most_frequent_country(autocomplete_data)
            location_info = []

            for item in autocomplete_data.get('data', []):
                if item['navigation']['entityType'] == 'AIRPORT' and item['presentation']['subtitle'] == country_choice:
                    sky_id = item['navigation']['relevantFlightParams']['skyId']
                    location_info.append(sky_id)

            flights_data = fetch_flights(departure_date.isoformat(), location_info)
            if flights_data:
                airports_details = []
                for flight in flights_data:
                    airport_info = get_airport_details(flight['arrival']['airport']['iata'])
                    if airport_info:
                        weather_info = get_weather(airport_info['latitude'], airport_info['longitude'])
                        # Details für jeden Flughafen sammeln
                        airports_details.append({
                            "Destination": airport_info['name'],
                            "IATA": flight['arrival']['airport']['iata'],
                            "Departure Time (UTC)": flight['departure']['date']['utc'],
                            "Latitude": airport_info['latitude'],
                            "Longitude": airport_info['longitude'],
                            "Weather Condition": weather_info['Condition'] if weather_info else "No data",
                            "Temperature (C)": weather_info['Temperature'] if weather_info else "No data"
                        })

                if airports_details:
                    st.write("Internationale Flüge gefunden:")
                    for airport in airports_details:
                        st.write(f"Destination: {airport['Destination']}, IATA: {airport['IATA']}, "
                                 f"Departure Time (UTC): {airport['Departure Time (UTC)']}, "
                                 f"Latitude: {airport['Latitude']}, Longitude: {airport['Longitude']}, "
                                 f"Weather Condition: {airport['Weather Condition']}, "
                                 f"Temperature (C): {airport['Temperature (C)']}")
                else:
                    st.write("Details zu den Flughäfen konnten nicht abgerufen werden.")
            else:
                st.write("Keine internationalen Flüge gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()

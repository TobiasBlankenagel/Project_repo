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

# Sammelt Flughafeninformationen nach Land
def process_and_collect_locations(data, country_choice):
    location_info = []
    if data and 'data' in data:
        for item in data['data']:
            if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT' and item['presentation']['subtitle'].endswith(country_choice):
                iata_code = item['navigation']['relevantFlightParams']['skyId']
                location_info.append((iata_code))
    return location_info

# Abfrage der Flugdaten für ein bestimmtes Datum und mehrere IATA-Codes
def fetch_flights(departure_date, locations):
    flights_data = []
    url = "https://flight-info-api.p.rapidapi.com/schedules"
    headers = {
        "X-RapidAPI-Key": "1ebd07a20dmsh3d8c30c0e64a87ep15d844jsn48cdaa310b4a",
        "X-RapidAPI-Host": "flight-info-api.p.rapidapi.com"
    }

    # Ausgabe der JSON-Datei für location_info
   #st.write("JSON-Datei für location_info:")
   #st.json(locations) # hier wird eine Liste von IATA-Codes ausgegeben
    
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
            # st.json(data)
            # Filter out domestic flights
            country_code = data[0]['departure']['country']['code']
            for flight in data:
                if flight['arrival']['country']['code'] != country_code:
                    flights_data.append(flight)
    return flights_data

def get_weather(lat, lon):
    # OpenWeather API URL
    url = "https://api.openweathermap.org/data/2.5/weather"
    # API-Schlüssel und Koordinaten hinzufügen
    params = {
        "lat": lat,
        "lon": lon,
        "appid": "afe025cb2b8a2785c5837a3eaed7b62a",  # Dein OpenWeather API-Key
        "units": "metric",  # Setzt die Temperatureinheit auf Celsius
        "lang": "de"  # Ergebnisse auf Deutsch
    }
    # Anfrage an die OpenWeather API senden
    response = requests.get(url, params=params)
    # Prüfe, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        weather = response.json()
        temperature = weather['main']['temp']  # Temperatur in Celsius
        condition = weather['weather'][0]['description']  # Wetterbeschreibung
        return {"Temperature": temperature, "Condition": condition}
    return None


# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Suche für Flughäfen, Flugdatenabfrage und Wetterinformationen')

    query = st.text_input('Geben Sie einen Standort ein, z.B. London', '')
    if query:
        autocomplete_data = fetch_autocomplete_data(query)
        if autocomplete_data:
            countries = sorted({item['presentation']['subtitle'].split(',')[-1].strip() for item in autocomplete_data.get('data', []) if item['navigation']['entityType'] == 'AIRPORT'})
            country_choice = st.selectbox('Wählen Sie ein Land aus', countries)
            departure_date = st.date_input('Wählen Sie ein Abflugdatum', min_value=date.today())
            if st.button("Suche starten"):
                location_info = process_and_collect_locations(autocomplete_data, country_choice)
                if location_info:
                    flights_data = fetch_flights(departure_date.isoformat(), location_info)
                    if flights_data:
                        st.write("Internationale Flüge gefunden:")
                        airports_details = []
                        for flight in flights_data:
                            iata_code = flight['arrival']['airport']['iata']
                            airport_data = get_airport_details(iata_code)
                            if airport_data:
                                latitude = airport_data['latitude']
                                longitude = airport_data['longitude']
                                weather = get_weather(latitude, longitude) # muss geändert werden, da unbegrenzte api requests
                                airports_details.append({
                                    "IATA": iata_code,
                                    "Latitude": latitude,
                                    "Longitude": longitude,
                                    "Weather": weather
                                })
                        st.write(airports_details)
                    else:
                        st.write("Keine internationalen Flüge gefunden.")
                else:
                    st.write("Keine Flughäfen im gewählten Land gefunden.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie die Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()
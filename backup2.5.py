import streamlit as st
import requests
from datetime import date
import base64
# Autocomplete Suchleiste für Nutzer
import time



def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "DE", "locale": "de-DE"}
    headers = {
        "X-RapidAPI-Key": "bd2791b14fmsh26f690b30808f74p1470d4jsn29b1b6dceb93",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    time.sleep(1)  # Verzögerung, um weniger wie ein Bot zu wirken
    response = requests.get(url, headers=headers, params=querystring)
    st.write(response)
    if response.status_code == 200:
        data = response.json()
        st.json(data)
        if 'message' in data and 'redirect_to' in data['message']:
            redirect_url = data['message']['redirect_to']
            # Decode URL if needed (assuming it's base64 encoded)
            if 'url' in redirect_url:
                base_url = "https://skyscanner80.p.rapidapi.com"  # Base URL for the API
                full_url = base_url + redirect_url
                st.markdown(f"Please verify you are not a robot by clicking [here]({full_url}) and completing the CAPTCHA.")
            else:
                st.error("You are being rate limited or blocked. Please try again later.")
        return data
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    







# Fetch airport details like latitude and longitude using IATA code
def get_airport_details(iata_code):
    url = f"https://aviation-reference-data.p.rapidapi.com/airports/{iata_code}"
    headers = {
        "X-RapidAPI-Key": "bd2791b14fmsh26f690b30808f74p1470d4jsn29b1b6dceb93",
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
        "X-RapidAPI-Key": "bd2791b14fmsh26f690b30808f74p1470d4jsn29b1b6dceb93",
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
                if flight_key not in seen_flights:  # Prüft, ob der Flug bereits gesehen wurde
                    flights_data.append(flight)
                    seen_flights.add(flight_key)  # Fügt den Flug zum Set der gesehenen Flüge hinzu

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
    # Increases the range to 30000 meters to find the largest nearby city
    querystring = {"latitude": str(lat), "longitude": str(lon), "range": "30000"}
    headers = {
        "X-RapidAPI-Key": "bd2791b14fmsh26f690b30808f74p1470d4jsn29b1b6dceb93",
        "X-RapidAPI-Host": "geocodeapi.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                largest_city = data[0].get('City', 'Unknown City')
                return largest_city
            else:
                return 'No data available'
        else:
            return f"Error fetching data: Status Code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    # Einrichten der Seitenleiste für die Navigation zwischen verschiedenen Funktionen
    st.sidebar.title("Menü")
    app_modus = st.sidebar.selectbox("Wähle eine Option", ["Flüge suchen", "Temperaturkarte anzeigen", "Packliste"])

    if app_modus == "Flüge suchen":
        suche_fluege()
    elif app_modus == "Temperaturkarte anzeigen":
        st.sidebar.write("Das Feature für die Temperaturkarte wird hier hinzugefügt.")
    elif app_modus == "Packliste":
        st.sidebar.write("Das Feature für die Packliste wird hier hinzugefügt.")

def suche_fluege():
    st.title('Suche dein Reiseerlebnis!')

    standort = st.text_input('Gib einen Standort ein', '')
    abflugdatum = st.date_input('Wähle ein Abflugdatum', min_value=date.today())
    min_temp = st.number_input('Mindesttemperatur (°C) am Zielort', format="%d", step=1)
    max_temp = st.number_input('Höchsttemperatur (°C) am Zielort', format="%d", step=1)

    if st.button("Suche starten") and standort:
        autocomplete_daten = fetch_autocomplete_data(standort)
        if autocomplete_daten is None:
            return
        if autocomplete_daten:
            land_auswahl = get_most_frequent_country(autocomplete_daten)
            standort_info = [item['navigation']['relevantFlightParams']['skyId'] for item in autocomplete_daten.get('data', []) if item['navigation']['entityType'] == 'AIRPORT' and item['presentation']['subtitle'] == land_auswahl]
            flugdaten = fetch_flights(abflugdatum.isoformat(), standort_info)
            flughafen_details = []
            for flug in flugdaten:
                flughafen_info = get_airport_details(flug['arrival']['airport']['iata'])
                if flughafen_info:
                    stadt_name = get_city_by_coordinates(flughafen_info['latitude'], flughafen_info['longitude'])
                    wetter_info = get_weather(flughafen_info['latitude'], flughafen_info['longitude'])
                    flughafen_details.append({
                        "Zielort": stadt_name,
                        "IATA": flug['arrival']['airport']['iata'],
                        "Abflugzeit (lokal)": flug['departure']['time']['local'],
                        "Latitude": flughafen_info['latitude'],
                        "Longitude": flughafen_info['longitude'],
                        "Wetterzustand": wetter_info['weather'][0]['description'] if wetter_info else "Keine Daten",
                        "Temperatur (C)": wetter_info['main']['temp'] if wetter_info else "Keine Daten"
                    })

            gefilterte_fluege = filter_flights_by_temperature(flughafen_details, min_temp if min_temp != 0 else None, max_temp if max_temp != 0 else None)
            if gefilterte_fluege:
                st.write("Gefilterte Flüge gefunden:")
                for flug in gefilterte_fluege:
                    with st.expander(f"Flug nach {flug['Zielort']} (IATA: {flug['IATA']})"):
                        st.write(f"Abflugzeit (lokal): {flug['Abflugzeit (lokal)']}")
                        st.write(f"Latitude: {flug['Latitude']}, Longitude: {flug['Longitude']}")
                        st.write(f"Wetter: {flug['Wetterzustand']} bei {flug['Temperatur (C)']} °C")
                        if st.button("Mehr Details", key=flug['IATA']):
                            display_flight_details(flug['IATA'])
            else:
                st.write("Keine Flüge gefunden, die den Temperaturkriterien entsprechen.")
        else:
            st.error("Keine Antwort von der API. Überprüfen Sie Ihre Netzwerkverbindung oder API-Schlüssel.")

if __name__ == "__main__":
    main()


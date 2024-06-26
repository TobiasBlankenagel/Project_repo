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

# Findet die Flugdaten über Skyscanner API basierend auf airport ID und Ablugsdatum
def fetch_flights(from_id, depart_date):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-everywhere"
    querystring = {
        "fromId": from_id,
        "departDate": depart_date,
        "adults": "1",
        "currency": "EUR",
        "market": "DE",
        "locale": "de-DE"
    }
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json() if response.status_code == 200 else None


# speichert die gefundenen Airports ab
def process_and_save_autocomplete_data(data):
    if data and 'data' in data and data['data']:
        st.write("Found airports and related entities:")
        airports = []
        for item in data['data']:
            id = item.get('id', 'N/A')
            title = item['presentation']['title']
            subtitle = item['presentation']['subtitle']
            st.write(f"ID: {id}, Title: {title}, Subtitle: {subtitle}")
            if item['navigation']['entityType'] == 'AIRPORT':
                airports.append({'id': id, 'title': title})
        if airports:
            st.session_state['airports'] = airports
            st.write("Airports saved!")
        else:
            st.write("No airports to save found.")
    else:
        st.error("No data found or unexpected response structure.")


# Filtert die Informationen heraus, basierend auf den gefundenen Flügen in fetch_flights
def fetch_all_flights():
    if 'airports' in st.session_state and st.session_state['airports'] and 'depart_date' in st.session_state:
        flights_info = []
        destinations = []
        for airport in st.session_state['airports']:
            flight_data = fetch_flights(airport['id'], st.session_state['depart_date'].isoformat())
            if flight_data:
                flights_info.append(flight_data)
                for result in flight_data['data']['everywhereDestination']['results']:
                    if 'content' in result and 'location' in result['content'] and 'id' in result['content']['location']:
                        destinations.append(result['content']['location']['id'])
        if flights_info:
            st.write("Found flights from all saved airports:")
            for info in flights_info:
                st.json(info)
            display_destinations(destinations)  # Call to display destinations
        else:
            st.write("No flights found.")
    else:
        st.error("No saved airports or date. Please save airports and select a date.")


# entityid codes auflisten
def fetch_geo_data():
    url = "https://partners.api.skyscanner.net/apiservices/v3/geo/hierarchy/flights/de-DE"
    headers = {
        "x-api-key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a" 
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 401:
        st.error("Unauthorized. Check your API key and permissions.")
    elif response.status_code != 200:
        st.error(f"Failed to fetch data. Status Code: {response.status_code}")
    else:
        data = response.json()
        if 'places' in data:
            st.write("Geographical Locations (Entity IDs and Names):")
            for place in data['places']:
                st.write(f"Entity ID: {place['entityId']}, Name: {place['name']}")
        else:
            st.error("No places found in the response.")


# Funktion, um herauszufinden an welchen Ort die Flüge fliegen
def display_destinations(destinations):
    if destinations:
        st.write("Destinations (Entity IDs):")
        for destination in destinations:
            st.write(destination)
    else:
        st.write("No destinations found.")



# Funktion um das Wetter an den Orten zu checken und zwischenzuspeichern, welche Orte mit den eigenen Präferenzen übereinstimmen






# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Search for Flights from a Location')

    if st.button("Fetch Geo Data"):
        locale = 'de-DE'
        fetch_geo_data()

    if 'airports' not in st.session_state:
        st.session_state['airports'] = []

    with st.form("search_form"): # Suchformular
        query = st.text_input('Enter a location', '')
        depart_date = st.date_input("Choose departure date for all flights", min_value=date.today())
        submitted = st.form_submit_button("Magische Suche")

        if submitted: # wenn abgesendet...
            st.session_state['depart_date'] = depart_date  # speichert das Datum in Session
            autocomplete_data = fetch_autocomplete_data(query) # führt die autocomplete Funktion aus
            st.write("API response data:")
            st.json(autocomplete_data) # zeigt kurz Json Datei an
            process_and_save_autocomplete_data(autocomplete_data)  # führt Funktion aus, um die gefundenen Airpots zu speichern
            fetch_all_flights() # filtert die Infos zu den gefundenen Flügen vom Airport raus
        

if __name__ == "__main__":
    main()







def get_city_by_coordinates(lat, lon):
    url = "https://geocodeapi.p.rapidapi.com/GetNearestCities"
    querystring = {"latitude": str(lat), "longitude": str(lon), "range": "30000"}
    headers = {
        "X-RapidAPI-Key": "89fa2cdc22mshef83525ac6af5ebp10c163jsnc8047ffa3882",
        "X-RapidAPI-Host": "geocodeapi.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            st.json(data)
            if data and isinstance(data, list) and len(data) > 0:
                nearest_city = data[0].get('City', 'Unknown City')
                return nearest_city
            else:
                return 'No data available'
        else:
            return f"Error fetching data: Status Code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"





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

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
    url = "https://partners.api.skyscanner.net//apiservices/v3/geo/hierarchy/flights", 
    headers = {
        "Accept": "application/json",
        "x-api-key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a"  # Your API key
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
        fetch_geo_data(locale)

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

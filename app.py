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
        for airport in st.session_state['airports']:
            flight_data = fetch_flights(airport['id'], st.session_state['depart_date'].isoformat())
            if flight_data:
                flights_info.append(flight_data)
        if flights_info:
            st.write("Found flights from all saved airports:")
            for info in flights_info:
                st.json(info)
                display_destination_by_entityId(info)  # New function call to display destinations
        else:
            st.write("No flights found.")
    else:
        st.error("No saved airports or date. Please save airports and select a date.")



# Funktion, um herauszufinden an welchen Ort die Flüge fliegen
def display_destination_by_entityId(flights_info):
    if flights_info and 'places' in flights_info and 'quotes' in flights_info:
        places = {place['entityId']: place for place in flights_info['places']}
        for quote in flights_info['quotes']:
            if 'destinationId' in quote:
                destination_id = quote['destinationId']
                if destination_id in places:
                    destination_place = places[destination_id]
                    st.write(f"Destination: {destination_place['name']} - Price: {quote['price']}")
    else:
        st.write("No detailed destination data available.")



# Funktion um das Wetter an den Orten zu checken und zwischenzuspeichern, welche Orte mit den eigenen Präferenzen übereinstimmen






# Hauptfunktion zum Laufen auf Streamlit
def main():
    st.title('Auto-Complete Search for Flights from a Location')
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

import streamlit as st
import requests
from datetime import datetime

# Konfigurieren der API-Schlüssel und Header
headers = {
    "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
    "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
}

# Funktion zum Abrufen der Autocomplete-Daten
def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "DE", "locale": "de-DE"}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Funktion zum Abrufen der One-Way-Flugdaten
def fetch_one_way_flights(from_id, to_id, depart_date):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way"
    querystring = {
        "fromId": from_id,
        "toId": to_id,
        "departDate": depart_date,
        "adults": "1",
        "currency": "EUR",
        "market": "DE",
        "locale": "de-DE"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Streamlit-Seite aufbauen
def main():
    st.title("One-Way Flight Search")
    
    # Eingabefelder für Flughäfen und Datum
    from_query = st.text_input("From (airport):", "Type to search...")
    to_query = st.text_input("To (airport):", "Type to search...")
    depart_date = st.date_input("Departure Date", min_value=datetime.today())

    if st.button("Search Flights"):
        # Autocomplete für Flughäfen
        from_data = fetch_autocomplete_data(from_query)
        to_data = fetch_autocomplete_data(to_query)
        
        # Ermitteln der ersten ID aus den Autocomplete-Daten (hier wäre eine bessere Auswahllogik angebracht)
        from_id = from_data['data'][0]['id'] if 'data' in from_data and len(from_data['data']) > 0 else None
        to_id = to_data['data'][0]['id'] if 'data' in to_data and len(to_data['data']) > 0 else None

        # Flugdaten abrufen, wenn beide IDs vorhanden sind
        if from_id and to_id:
            flights = fetch_one_way_flights(from_id, to_id, depart_date.isoformat())
            st.write("Flight Data (JSON):")
            st.json(flights)
        else:
            st.error("Could not retrieve IDs for both airports. Please check your input.")

if __name__ == "__main__":
    main()

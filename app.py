import streamlit as st
import requests
import pandas as pd
from datetime import date

def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def fetch_flights(city_id, depart_date):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-everywhere"
    querystring = {
        "fromId": city_id,
        "departDate": depart_date,
        "adults": "1",
        "currency": "USD",
        "market": "US",
        "locale": "en-US"
    }
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Fehler bei der Flugabfrage: {response.status_code} - {response.text}")
        return None

def display_flights(flights_data):
    if flights_data:
        st.write("Gesamte Antwortdaten von der API:")
        st.json(flights_data)  # Zeigt die gesamte Antwort als JSON im Interface

        if 'data' in flights_data and flights_data['data'].get('everywhereDestination'):
            flights = flights_data['data']['everywhereDestination']['results']
            if flights:
                df = pd.DataFrame(flights)
                st.write("Nächste Flüge vom ausgewählten Ort:")
                st.dataframe(df)
            else:
                st.error("Keine Flüge gefunden.")
        else:
            st.error("Fehler in den Flugdaten oder unerwartete Struktur der API-Antwort.")
    else:
        st.error("Keine Antwortdaten erhalten.")

def main():
    st.title('Auto-Complete Suche für Flüge von einem Ort')
    with st.form("search_form"):
        query = st.text_input('Geben Sie einen Ort ein', 'New York')
        depart_date = st.date_input("Wählen Sie das Abflugdatum", min_value=date.today())
        submitted = st.form_submit_button("Flüge suchen")
        
        if submitted:
            autocomplete_data = fetch_autocomplete_data(query)
            if 'data' in autocomplete_data and any(item["navigation"]["entityType"] == "AIRPORT" for item in autocomplete_data['data']):
                city_id = autocomplete_data['data'][0]['navigation']['id']  # Assumes the first airport ID corresponds to the city
                flights_data = fetch_flights(city_id, depart_date.isoformat())
                display_flights(flights_data)
            else:
                st.error("Keine Flughäfen gefunden für den eingegebenen Ort.")

if __name__ == "__main__":
    main()

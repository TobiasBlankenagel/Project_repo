import streamlit as st
import requests
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

def fetch_flights(from_id, depart_date):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-everywhere"
    querystring = {
        "fromId": from_id,
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
    return response.json() if response.status_code == 200 else None

def display_autocomplete_results(data):
    if data and 'data' in data and data['data']:
        st.write("Gefundene Flughäfen und zugehörige Entitäten:")
        for item in data['data']:
            st.write(f"ID: {item.get('id', 'N/A')}, Titel: {item['presentation']['title']}, Untertitel: {item['presentation']['subtitle']}")
    else:
        st.error("Keine Daten gefunden oder unerwartete Antwortstruktur.")

def save_airports(data):
    if 'data' in data:
        airports = [{'id': item['id'], 'title': item['presentation']['title']} for item in data['data'] if item['navigation']['entityType'] == 'AIRPORT']
        if airports:
            st.session_state['airports'] = airports
            st.write("Flughäfen gespeichert!")
        else:
            st.write("Keine Flughäfen zum Speichern gefunden.")
    else:
        st.error("Keine Daten zum Speichern verfügbar.")

def fetch_all_flights():
    if 'airports' in st.session_state and st.session_state['airports']:
        flights_info = []
        depart_date = st.date_input("Wählen Sie das Abflugdatum für alle Flüge", min_value=date.today())
        if st.button("Alle Flüge finden"):
            for airport in st.session_state['airports']:
                flight_data = fetch_flights(airport['id'], depart_date.isoformat())
                if flight_data:
                    flights_info.append(flight_data)
            if flights_info:
                st.write("Gefundene Flüge von allen gespeicherten Flughäfen:")
                for info in flights_info:
                    st.json(info)
            else:
                st.write("Keine Flüge gefunden.")
    else:
        st.error("Keine gespeicherten Flughäfen vorhanden. Bitte erst Flughäfen speichern.")

def main():
    st.title('Auto-Complete Suche für Flüge von einem Ort')
    if 'airports' not in st.session_state:
        st.session_state['airports'] = []

    with st.form("search_form"):
        query = st.text_input('Geben Sie einen Ort ein', 'New York')
        submitted = st.form_submit_button("Daten anzeigen und speichern")

        if submitted:
            autocomplete_data = fetch_autocomplete_data(query)
            st.write("API-Antwortdaten:")
            st.json(autocomplete_data)
            display_autocomplete_results(autocomplete_data)
            save_airports(autocomplete_data)

    fetch_all_flights()

if __name__ == "__main__":
    main()

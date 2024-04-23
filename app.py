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

def display_airports(data):
    if 'data' in data:
        airports = [item for item in data['data'] if item["navigation"]["entityType"] == "AIRPORT"]
        if airports:
            st.write("Wählen Sie einen Flughafen aus der Liste:")
            option = st.selectbox('Flughäfen:', airports, format_func=lambda x: f"{x['presentation']['title']} ({x['navigation']['localizedName']})")
            return option
        else:
            st.error("Keine Flughäfen gefunden.")
    else:
        st.error("Keine Daten gefunden.")

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
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Fehler bei der Flugabfrage: {response.status_code} - {response.text}")
        return None

def display_flights(flights_data):
    if flights_data:
        st.write("Gesamte Antwortdaten von der API:")
        st.json(flights_data)  # Zeigt die gesamte Antwort als JSON im Interface

        if 'data' in flights_data:
            flights = flights_data['data']['results']
            if flights:
                df = pd.DataFrame(flights)
                st.write("Nächste Flüge vom ausgewählten Flughafen:")
                st.dataframe(df)
            else:
                st.error("Keine Flüge gefunden.")
        else:
            st.error("Fehler in den Flugdaten oder unerwartete Struktur der API-Antwort.")
    else:
        st.error("Keine Antwortdaten erhalten.")


def main():
    st.title('Auto-Complete Suche für Flughäfen und Flüge')
    query = st.text_input('Geben Sie einen Flughafen ein', 'New York')

    if st.button('Flughafen suchen'):
        autocomplete_data = fetch_autocomplete_data(query)
        selected_airport = display_airports(autocomplete_data)
        if selected_airport:
            depart_date = st.date_input("Wählen Sie das Abflugdatum", min_value=date.today())
            flights_data = fetch_flights(selected_airport["id"], depart_date.isoformat())
            display_flights(flights_data)

if __name__ == "__main__":
    main()

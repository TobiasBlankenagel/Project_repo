import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json() if response.status_code == 200 else None

def fetch_flights(from_id, depart_date):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way"
    querystring = {
        "fromId": from_id,
        "departDate": depart_date.strftime('%Y-%m-%d'),
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

def display_results(data):
    if data and 'data' in data:
        airports = [item for item in data['data'] if item['navigation']['entityType'] == 'AIRPORT']
        if airports:
            df = pd.DataFrame({
                "ID": [item['id'] for item in airports],
                "Name": [item['presentation']['title'] for item in airports],
                "Entity ID": [item['navigation']['entityId'] for item in airports]
            })
            st.write(df)
            return df
        else:
            st.error("Keine Flughäfen gefunden.")
    else:
        st.error("Keine Ergebnisse gefunden.")

def main():
    st.title('Auto-Complete Suche für Flughäfen und Städte')
    query = st.text_input('Geben Sie einen Standort ein', 'New York')

    if st.button('Suche'):
        result = fetch_autocomplete_data(query)
        df = display_results(result)
        selected_id = st.selectbox('Wählen Sie einen Flughafen', df['Entity ID']) if df is not None else None
        depart_date = st.date_input('Abflugdatum', min_value=datetime.today())

        if st.button('Finde Flüge'):
            if selected_id:
                flights = fetch_flights(selected_id, depart_date)
                if flights and 'Quotes' in flights:
                    st.write(flights['Quotes'])
                elif flights:
                    st.write("Keine Flüge gefunden.")
                else:
                    st.error("Fehler bei der Flugsuche.")
            else:
                st.error('Bitte wählen Sie einen Flughafen aus.')

if __name__ == "__main__":
    main()

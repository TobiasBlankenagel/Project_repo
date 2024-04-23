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
        st.write("Found airports and related entities:")
        for item in data['data']:
            st.write(f"ID: {item.get('id', 'N/A')}, Title: {item['presentation']['title']}, Subtitle: {item['presentation']['subtitle']}")
    else:
        st.error("No data found or unexpected response structure.")

def save_airports(data):
    if 'data' in data:
        airports = [{'id': item['id'], 'title': item['presentation']['title']} for item in data['data'] if item['navigation']['entityType'] == 'AIRPORT']
        if airports:
            st.session_state['airports'] = airports
            st.write("Airports saved!")
        else:
            st.write("No airports to save found.")
    else:
        st.error("No data to save available.")

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
        else:
            st.write("No flights found.")
    else:
        st.error("No saved airports or date. Please save airports and select a date.")

def main():
    st.title('Auto-Complete Search for Flights from a Location')
    if 'airports' not in st.session_state:
        st.session_state['airports'] = []

    with st.form("search_form"):
        query = st.text_input('Enter a location', 'New York')
        depart_date = st.date_input("Choose departure date for all flights", min_value=date.today())
        submitted = st.form_submit_button("Display and Save Data")

        if submitted:
            st.session_state['depart_date'] = depart_date  # Save the departure date
            autocomplete_data = fetch_autocomplete_data(query)
            st.write("API response data:")
            st.json(autocomplete_data)
            display_autocomplete_results(autocomplete_data)
            save_airports(autocomplete_data)

    if st.button("Find Flights from Saved Airports"):
        fetch_all_flights()

if __name__ == "__main__":
    main()

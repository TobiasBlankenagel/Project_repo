import streamlit as st
import requests
from datetime import date

# Fetches autocomplete data for flight locations based on user input
def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Fetches flight data from the Skyscanner API based on the given airport ID and departure date
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


# Fetches flight information for all saved airports on the selected date
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


# Main function to run the Streamlit application
def main():
    st.title('Auto-Complete Search for Flights from a Location')
    if 'airports' not in st.session_state:
        st.session_state['airports'] = []

    with st.form("search_form"):
        query = st.text_input('Enter a location', '')
        depart_date = st.date_input("Choose departure date for all flights", min_value=date.today())
        submitted = st.form_submit_button("Magische Suche")

        if submitted:
            st.session_state['depart_date'] = depart_date  # Save the departure date
            autocomplete_data = fetch_autocomplete_data(query)
            st.write("API response data:")
            st.json(autocomplete_data)
            process_and_save_autocomplete_data(autocomplete_data)  # Using the new merged function
            fetch_all_flights()
        

if __name__ == "__main__":
    main()

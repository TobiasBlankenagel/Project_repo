import streamlit as st
import requests

def fetch_airport_data(query):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport"
    querystring = {"query": query}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API returned a status code {response.status_code}: {response.text}"}

def fetch_flights(from_id, depart_date):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport"  # This URL might be incorrect for flight search
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
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json() if response.status_code == 200 else {"error": "Failed to fetch flights"}

def main():
    st.title('Travel Search Engine')
    
    st.subheader('Airport Information Search')
    query = st.text_input('Enter a city to search for its airports', 'London')
    if st.button('Search Airports', key='1'):
        results = fetch_airport_data(query)
        if 'error' in results:
            st.error("Failed to fetch data: " + results['error'])
        else:
            st.write(results)

    st.subheader('Flight Search')
    from_id = st.text_input('Enter airport ID for departure', '12345')
    depart_date = st.text_input('Enter departure date (YYYY-MM-DD)', '2023-01-01')
    if st.button('Search Flights', key='2'):
        flight_results = fetch_flights(from_id, depart_date)
        if 'error' in flight_results:
            st.error("Failed to fetch data: " + flight_results['error'])
        else:
            st.write(flight_results)

if __name__ == "__main__":
    main()

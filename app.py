import streamlit as st
import requests

def fetch_flight_destinations(query):
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination"
    querystring = {"query": query}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def main():
    st.title('Flight Destination Search')
    query = st.text_input('Enter a keyword for flight destinations', 'New')
    if st.button('Search Destinations'):
        results = fetch_flight_destinations(query)
        if 'errors' in results:
            st.error("Error: " + str(results['errors']))
        else:
            st.write(results)

if __name__ == "__main__":
    main()

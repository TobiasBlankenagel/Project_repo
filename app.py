import streamlit as st
import requests

def fetch_airport_data(location):
    url = "https://travel-advisor.p.rapidapi.com/airports/search"
    querystring = {"query": location, "locale": "en_US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def fetch_location_data(query):
    url = "https://travel-advisor.p.rapidapi.com/locations/v2/auto-complete"
    querystring = {"query": query, "lang": "en_US", "units": "km"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def main():
    st.title('Travel Advisor Search')
    st.subheader('Search for Airports and Popular Locations')

    col1, col2 = st.columns(2)
    with col1:
        st.header("Airport Search")
        location = st.text_input("Enter a location for airports", "New York")
        if st.button("Search Airports", key='1'):
            results = fetch_airport_data(location)
            st.write(results)

    with col2:
        st.header("Location Search")
        query = st.text_input("Enter a location or landmark", "Eiffel Tower")
        if st.button("Search Location", key='2'):
            results = fetch_location_data(query)
            st.write(results)

if __name__ == "__main__":
    main()

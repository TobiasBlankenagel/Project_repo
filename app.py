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

def main():
    st.title('Airport Search')
    location = st.text_input('Enter a location:', 'New York')
    if st.button('Search'):
        results = fetch_airport_data(location)
        st.write(results)

if __name__ == "__main__":
    main()

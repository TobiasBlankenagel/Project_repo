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

def extract_short_names(results):
    # Sicherstellen, dass die notwendigen Schlüssel vorhanden sind und vermeiden von IndexError
    if 'data' in results and len(results['data']) > 0 and 'children' in results['data'][0]:
        return [child['shortName'] for child in results['data'][0]['children']]
    else:
        return []

def main():
    st.title('Airport Information Search')
    query = st.text_input('Enter a city to search for its airports', 'London')
    if st.button('Search Airports'):
        results = fetch_airport_data(query)
        if 'error' in results:
            st.error("Failed to fetch data: " + results['error'])
        else:
            airport_names = extract_short_names(results)
            st.write("Airport Short Names:", airport_names)

if __name__ == "__main__":
    main()

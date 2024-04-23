import streamlit as st
import requests

def fetch_flight_destinations(query):
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination"
    querystring = {"query": query}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned a status code {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    st.title('Flight Destination Search')
    query = st.text_input('Enter a keyword for flight destinations', 'New')
    if st.button('Search Destinations'):
        results = fetch_flight_destinations(query)
        if 'error' in results:
            st.error("Failed to fetch data: " + results['error'])
        elif results.get('status') == False:
            st.error(f"Error from API: {results.get('message', 'No error message provided.')}")
        else:
            st.write(results)

if __name__ == "__main__":
    main()

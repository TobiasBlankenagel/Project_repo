import streamlit as st
import requests
import json
import pandas as pd

# API configuration
api_url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
headers = {
    "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
    "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
}

def fetch_airports(query):
    """ Fetch airports from Skyscanner autocomplete API. """
    params = {"query": query, "market": "US", "locale": "en-US"}
    response = requests.get(api_url, headers=headers, params=params)
    return response.json()

def collect_airports():
    """ Collects airports data from A to Z and stores them in a DataFrame. """
    letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    airports_list = []

    for letter in letters:
        result = fetch_airports(letter)
        if 'data' in result:
            for item in result['data']:
                if 'navigation' in item and item['navigation']['entityType'] == 'AIRPORT':
                    id = item['id']
                    name = item['presentation']['title']
                    airports_list.append({'ID': id, 'Name': name, 'Letter': letter})

    return pd.DataFrame(airports_list)

def main():
    """ Main function to run Streamlit app. """
    st.title('Airport Entity ID Collector')
    st.subheader('Collect and display airports entity IDs from A to Z')

    if st.button('Fetch Airport Data'):
        airports_df = collect_airports()
        st.write('Collected Airport Data:')
        st.dataframe(airports_df)

        # Optionally save to CSV
        if st.button('Save to CSV'):
            airports_df.to_csv('airports_entity_ids.csv', index=False)
            st.success('Data saved to airports_entity_ids.csv')

if __name__ == "__main__":
    main()

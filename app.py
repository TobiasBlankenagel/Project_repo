import streamlit as st
import requests

def fetch_airport_data(query):
    url = "https://priceline-com-provider.p.rapidapi.com/v2/flight/autoComplete"
    querystring = {
        "string": query,
        "airports": "true"
    }
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "API returned a status code {}: {}".format(response.status_code, response.text)}

def extract_airport_names(data):
    airport_list = []
    if data:
        results = data.get('getAirAutoComplete', {}).get('results', {}).get('getSolr', {}).get('results', {}).get('data', {}).get('airport_data', {})
        for key, airport in results.items():
            if key.startswith('airport_'):
                name = airport.get('airport', 'Unknown Airport')
                iata = airport.get('iata', 'N/A')
                airport_list.append((name, iata))
    return airport_list


def main():
    st.title('Airport Search Tool')
    query = st.text_input('Enter a city name to search for airports:', 'London')
    if st.button('Search'):
        result = fetch_airport_data(query)
        st.write(result)
        if 'error' in result:
            st.error(result['error'])
        else:
            airport_names = extract_airport_names(result)
            if airport_names:
                st.write("Airports in {}: ".format(query))
                for name in airport_names:
                    st.write(name)
            else:
                st.write("No airports found for the city.")

if __name__ == "__main__":
    main()

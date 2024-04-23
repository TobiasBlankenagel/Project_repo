import streamlit as st
import requests

def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.title('Flughafen Autovervollständigung')
    query = st.text_input('Geben Sie einen Suchbegriff ein', 'new')
    
    if st.button('Suche'):
        result = fetch_autocomplete_data(query)
        if result:
            st.write(result)
        else:
            st.error('Keine Ergebnisse gefunden oder Fehler bei der Anfrage.')

if __name__ == "__main__":
    main()

import streamlit as st
import requests
import pandas as pd

def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json() if response.status_code == 200 else None

def display_results(data):
    if data and 'Places' in data:
        places = data['Places']
        df = pd.DataFrame(places)
        st.table(df)
    else:
        st.error("Keine Ergebnisse gefunden oder Fehler bei der API-Anfrage.")

def main():
    st.title('Flughafen Auto-Complete Suche')
    query = st.text_input('Geben Sie einen Suchbegriff ein (z.B. "New York")')

    if query:
        result = fetch_autocomplete_data(query)
        if result:
            display_results(result)
        else:
            st.error("Fehler bei der Anfrage. Bitte überprüfen Sie Ihre Eingabe oder versuchen Sie es später erneut.")

if __name__ == "__main__":
    main()

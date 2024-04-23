import streamlit as st
import requests
import pandas as pd

# Verbindung

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
    
# Daten zur Eingabe finden

def display_results(raw_response):
    if raw_response.status_code == 200:
        data = raw_response.json()
        st.write("Gesamte Antwortdaten:")
        st.json(data)  # Zeigt die gesamten JSON-Daten in einer ansprechbaren Form an

        if 'data' in data:
            items = data['data']
            df = pd.DataFrame.from_records([{
                "Title": item["presentation"]["title"],
                "Suggestion Title": item["presentation"]["suggestionTitle"],
                "Subtitle": item["presentation"]["subtitle"],
                "Localized Name": item["navigation"]["localizedName"],
                "Entity Type": item["navigation"]["entityType"],
                "Entity ID": item["navigation"]["entityId"],
                "From ID": item["navigation"]["fromID"]
            } for item in items if "navigation" in item])
            st.table(df)
        else:
            st.error("Keine Ergebnisse gefunden.")
    else:
        st.error(f"Fehler {raw_response.status_code}: {raw_response.text}")

# Eingabefeld

def main():
    st.title('Auto-Complete Suche für Flughäfen und Städte')
    query = st.text_input('Geben Sie einen Standort ein', 'New York')

    if st.button('Suche'):
        result = fetch_autocomplete_data(query)
        display_results(result)

if __name__ == "__main__":
    main()

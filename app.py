import streamlit as st
import requests
from datetime import date

def fetch_autocomplete_data(query):
    url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"
    querystring = {"query": query, "market": "US", "locale": "en-US"}
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def display_autocomplete_results(data):
    if data and 'data' in data and data['data']:
        airports = [item for item in data['data'] if 'id' in item]  # Liste aller Flughäfen mit ID
        if airports:
            st.write("Gefundene Flughäfen:")
            for airport in airports:
                st.write(f"ID: {airport['id']}, Ort: {airport['presentation']['title']} ({airport['presentation']['suggestionTitle']}), {airport['presentation']['subtitle']}")
        else:
            st.error("Keine Flughäfen gefunden.")
    else:
        st.error("Keine Daten gefunden oder unerwartete Antwortstruktur.")

def main():
    st.title('Auto-Complete Suche für Flüge von einem Ort')
    with st.form("search_form"):
        query = st.text_input('Geben Sie einen Ort ein', 'New York')
        depart_date = st.date_input("Wählen Sie das Abflugdatum", min_value=date.today())
        submitted = st.form_submit_button("Daten anzeigen")

        if submitted:
            autocomplete_data = fetch_autocomplete_data(query)
            st.write("API-Antwortdaten:")
            st.json(autocomplete_data)  # Zeigt die gesamte JSON-Antwort an
            display_autocomplete_results(autocomplete_data)

if __name__ == "__main__":
    main()

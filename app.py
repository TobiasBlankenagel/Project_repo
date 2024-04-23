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

            # Beispiel zum Suchen des ersten verfügbaren Flughafens mit 'id'
            if 'data' in autocomplete_data and any(item["navigation"]["entityType"] == "AIRPORT" for item in autocomplete_data['data']):
                for airport in autocomplete_data['data']:
                    if airport["navigation"]["entityType"] == "AIRPORT":
                        st.write("Gefundene Flughafen-ID:", airport["navigation"]["id"])
                        break
                else:
                    st.error("Keine Flughafen-ID in der Antwort gefunden.")
            else:
                st.error("Keine Flughäfen gefunden für den eingegebenen Ort.")

if __name__ == "__main__":
    main()

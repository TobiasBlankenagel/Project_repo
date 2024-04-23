import streamlit as st
import requests

def display_airports(data):
    if 'data' in data:
        airports = [item for item in data['data'] if item["navigation"]["entityType"] == "AIRPORT"]
        if airports:
            st.write("Wählen Sie einen Flughafen aus der Liste:")
            option = st.selectbox('Flughäfen:', airports, format_func=lambda x: f"{x['presentation']['title']} ({x['navigation']['localizedName']})")
            return option
        else:
            st.error("Keine Flughäfen gefunden.")
    else:
        st.error("Keine Daten gefunden.")

def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        st.write("Gesamte Antwortdaten von der API:")
        st.json(data)  # Zeigt die gesamte Antwort als JSON im Interface
        return data
    else:
        st.error("Fehler beim Laden der Daten von der API")
        return None

def main():
    st.title("Flughafen Viewer")
    api_url = st.text_input("Geben Sie die API-URL ein", value="https://example.com/api/flights")
    if st.button("Daten laden"):
        data = fetch_data(api_url)
        if data:
            selected_airport = display_airports(data)
            if selected_airport:
                st.write("Sie haben ausgewählt:", selected_airport)

if __name__ == "__main__":
    main()

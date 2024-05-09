import folium
import streamlit as st
import requests

def main():
    load_css()
    st.title("Wetterkarte")

    city = st.text_input("Gib einen Ort ein:", "")
    if city:
        lat, lon = fetch_location_data(city)
        if lat is not None:
            m = folium.Map(location=[lat, lon], zoom_start=12)
            folium.Marker([lat, lon], tooltip='Klicken für Wetterdetails').add_to(m)

            # Erstelle ein Map-Objekt
            map_data = m._repr_html_()
            st.components.v1.html(map_data, height=500)
        else:
            st.error("Keine Daten für den angegebenen Ort gefunden.")

def fetch_location_data(city):
    """ Funktion zum Abrufen der Koordinaten eines Ortes """
    api_key = 'Ihr_OpenWeatherMap_API_Schlüssel'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        return None, None

if __name__ == "__main__":
    main()

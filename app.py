import streamlit as st
import requests

def wetter_ort():
    st.title('Wetter nach Ort anzeigen')

    # Eingabefeld für den Ort
    ort = st.text_input('Gib einen Ort ein, um das Wetter zu überprüfen:', '')

    if ort and st.button('Wetter abrufen'):
        wetter_data = fetch_wetter(ort)
        if wetter_data:
            display_wetter(wetter_data, ort)
        else:
            st.error("Keine Wetterdaten verfügbar oder Fehler bei der Abfrage.")

def fetch_wetter(ort):
    """Holt Wetterdaten für den eingegebenen Ort."""
    api_key = "5609e5c95ae59033e36538f65e15b9da"  # Ersetzen Sie dies durch Ihren eigenen API-Schlüssel
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": ort,
        "appid": api_key,
        "units": "metric",
        "lang": "de"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_wetter(data, ort):
    """Zeigt das Wetter für den angegebenen Ort an."""
    temperatur = data['main']['temp']
    beschreibung = data['weather'][0]['description']
    wetter_icon_code = data['weather'][0]['icon']
    wetter_icon_url = f"http://openweathermap.org/img/w/{wetter_icon_code}.png"
    
    st.write(f"Temperatur in {ort}: {temperatur}°C")
    st.write(f"Wetterzustand: {beschreibung}")
    st.image(wetter_icon_url, caption=beschreibung)

def main():
    st.sidebar.title("Menü")
    app_modus = st.sidebar.selectbox("Wähle eine Option", ["Wetter nach Ort anzeigen"])

    if app_modus == "Wetter nach Ort anzeigen":
        wetter_ort()

# Implementierung anderer Funktionen bleibt wie zuvor

if __name__ == "__main__":
    main()

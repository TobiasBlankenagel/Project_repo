import requests

def check_api_status():
    url = 'https://skyscanner80.p.rapidapi.com/api/v1/checkServer'
    headers = {
        'X-RapidAPI-Key': 'dein-api-key-hier',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # gibt den Status des Servers zurück
        else:
            return "API nicht erreichbar"
    except requests.exceptions.RequestException as e:
        return str(e)  # Fehler als String zurückgeben


import streamlit as st

def main():
    st.title('Flugsuche')

    # Überprüfe zuerst die API-Verfügbarkeit
    status = check_api_status()
    if status.get('status'):
        st.success('API ist online: ' + status.get('message'))
        # Eingabefelder für die Benutzer
        from_airport = st.text_input('Abflughafen')
        to_airport = st.text_input('Zielflughafen')
        depart_date = st.date_input('Abflugdatum')

        if st.button('Flüge suchen'):
            if from_airport and to_airport and depart_date:
                # Hier würdest du deine Funktion zum Abrufen der Flugdaten aufrufen
                st.write('Suche Flüge...')
            else:
                st.error('Bitte alle erforderlichen Felder ausfüllen!')
    else:
        st.error('API ist derzeit nicht erreichbar: ' + status)

if __name__ == "__main__":
    main()

import requests

def fetch_one_way_flights(from_id, to_id, depart_date):
    url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way'
    headers = {
        'X-RapidAPI-Key': '20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }
    params = {
        'fromId': from_id,
        'toId': to_id,
        'departDate': depart_date,
        'adults': '1',
        'currency': 'USD',
        'market': 'US',
        'locale': 'en-US'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Löst eine Exception aus, wenn die Anfrage nicht erfolgreich war
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return None


import streamlit as st
from datetime import datetime

def main():
    st.title('One-Way Flugsuche')
    
    # Überprüfe zuerst die API-Verfügbarkeit
    status = check_api_status()
    if status.get('status'):
        st.success('API ist online: ' + status.get('message'))
        from_id = st.text_input('From ID (Base64 kodiert)')
        to_id = st.text_input('To ID (Base64 kodiert)')
        depart_date = st.date_input('Abflugdatum', min_value=datetime.today())
        
        if st.button('Suche Flüge'):
            if from_id and to_id and depart_date:
                result = fetch_one_way_flights(from_id, to_id, depart_date.strftime('%Y-%m-%d'))
                if result and 'Quotes' in result:
                    st.write(result['Quotes'])
                elif result:
                    st.write('Keine Flüge gefunden.')
                else:
                    st.error('Fehler bei der Flugsuche.')
            else:
                st.error('Bitte alle erforderlichen Felder ausfüllen!')
    else:
        st.error('API ist derzeit nicht erreichbar: ' + str(status))

if __name__ == "__main__":
    main()

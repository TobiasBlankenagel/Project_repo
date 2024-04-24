import streamlit as st
import requests

def fetch_data(airport_code=None):
    base_url = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json"
    if airport_code:
        base_url += f"?fAir={airport_code}"
    response = requests.get(base_url)
    return response.json()

def main():
    st.title("ADS-B Exchange Aircraft Tracker")
    airport_code = st.text_input("Enter airport code to filter (e.g., LHR for Heathrow):", "")
    if airport_code:
        data = fetch_data(airport_code)
    else:
        data = fetch_data()

    if 'acList' in data:
        st.json(data['acList'])
    else:
        st.write("No data found.")

if __name__ == "__main__":
    main()

import streamlit as st
import requests
import json

# Function to fetch flight data for multi-city flights
def fetch_flights_multi_city(legs, class_of_service, sort_order, currency_code):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlightsMultiCity"
    querystring = {
        "legs": json.dumps(legs),
        "classOfService": class_of_service,
        "sortOrder": sort_order,
        "currencyCode": currency_code
    }
    headers = {
        "X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Streamlit application
def main():
    st.title('Multi-City Flight Search')

    # User input for the flight search
    with st.form("flight_search"):
        # JSON input for legs
        legs_input = st.text_area("Enter flight legs in JSON format:", 
                                  '[{"sourceAirportCode":"BOS","destinationAirportCode":"LON","date":"2023-10-18"},{"sourceAirportCode":"LON","destinationAirportCode":"BOS","date":"2023-10-26"}]')
        class_of_service = st.selectbox("Class of Service", ["Economy", "Business", "First"])
        sort_order = st.selectbox("Sort Order", ["Price", "Duration"])
        currency_code = st.selectbox("Currency Code", ["USD", "EUR", "GBP"])
        submit_button = st.form_submit_button("Search Flights")

        if submit_button:
            try:
                # Parsing the JSON input for legs
                legs = json.loads(legs_input)
                result = fetch_flights_multi_city(legs, class_of_service, sort_order, currency_code)
                st.write("API Response:")
                st.json(result)
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please correct it and try again.")

if __name__ == "__main__":
    main()

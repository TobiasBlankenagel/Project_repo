import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import matplotlib.dates as mdates
import cachetools
import logging
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from requests.exceptions import HTTPError, RequestException

# Streamlit App Styling
def load_css():
    css = """
    <style>
        body {
            background-color: #f0f2f5;
            font-family: 'Arial', sans-serif;
            color: #333;
        }
        h1, h2 {
            color: #4a4e69;
            text-align: center;
        }
        .stButton>button {
            background-color: #4a4e69;
            color: white;
            font-size: 16px;
            border-radius: 20px;
            padding: 10px 24px;
            margin-top: 10px;
            width: 100%;
            transition: background-color 0.3s, color 0.3s;
        }
        .stButton>button:hover {
            background-color: #6c757d;
            color: #fff;
        }
        .stDataFrame {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }
        .stDataFrame th, .stDataFrame td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 12px;
            background-color: white;
            border-radius: 8px;
        }
        .stDataFrame th {
            background-color: #4a4e69;
            color: white;
            font-size: 16px;
        }
        .stDataFrame tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .stDataFrame tr:hover {
            box-shadow: 0 6px 10px 0 rgba(0,0,0,0.1);
            transform: scale(1.02);
            transition: transform 0.2s, box-shadow 0.2s;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Hard-coded credentials for APIs (For production, replace with environment variable retrieval)
AMADEUS_API_KEY = 'FARZ8tu1y4FxAY6b6YF7Zsv7s2rD4enn'
AMADEUS_API_SECRET = 'VKGiY566o3ofKsSf'
OPEN_WEATHER_API_KEY = '31861e6de17c0f294cfed4a59ed4eddf'

# API URLs setup for different Amadeus services
AMADEUS_API_URLs = {
    'base_url': "https://test.api.amadeus.com/v1",
    'flight_offers_search': "https://test.api.amadeus.com/v2",
    'flight_inspiration_search': "https://test.api.amadeus.com/v1",
    'airport_and_city_search': "https://test.api.amadeus.com/v1",
    'city_search': "https://test.api.amadeus.com/v1"
}

class AmadeusAPI:
    def __init__(self, api_key, api_secret, base_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.access_token = None
        self.token_expires = 0
        self.cache = cachetools.TTLCache(maxsize=100, ttl=3600)

    def authenticate(self):
        url = f"{self.base_url}/security/oauth2/token"
        payload = {
            'client_id': self.api_key,
            'client_secret': self.api_secret,
            'grant_type': 'client_credentials'
        }
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(url, data=payload)
                response.raise_for_status()
                json_data = response.json()
                self.access_token = json_data['access_token']
                self.token_expires = time.time() + json_data['expires_in']
                logging.info("Successfully authenticated with Amadeus API.")
                return self.access_token
            except HTTPError as e:
                logging.warning(f"HTTP error during authentication: {e.response.status_code} - {e.response.text}")
            except RequestException as e:
                logging.warning(f"Request error during authentication: {str(e)}")
            if attempt < retries - 1:
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                logging.info(f"Sleeping for {sleep_time:.2f} seconds before retrying.")
                time.sleep(sleep_time)
        logging.error("Failed to authenticate after multiple attempts.")
        return None

    def request_with_retry(self, url, params=None, method='get', retries=3):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        cache_key = f"{url}_{params}"
        if cache_key in self.cache:
            logging.debug(f"Cache hit for {cache_key}")
            return self.cache[cache_key]

        for attempt in range(retries):
            try:
                response = requests.request(
                    method,
                    url,
                    json=params if method == 'post' else None,
                    params=params if method == 'get' else None,
                    headers=headers
                )
                response.raise_for_status()
                json_response = response.json()
                self.cache[cache_key] = json_response
                return json_response
            except HTTPError as e:
                if response.status_code == 429:
                    sleep_time = (2 ** attempt) + random.uniform(0, 1) * 2  # Increase multiplier
                    logging.info(f"Sleeping for {sleep_time:.2f} seconds due to rate limiting.")
                    time.sleep(sleep_time)
                elif response.status_code == 500:
                    logging.error(f"Server error on attempt {attempt + 1}: {e} - {response.text}")
                    if attempt == retries - 1:
                        return None
                else:
                    logging.error(f"Non-retryable HTTP error on attempt {attempt + 1}: {e} - {response.text}")
                    break
            except RequestException as e:
                logging.error(f"Request error on attempt {attempt + 1}: {e}")
                if attempt == retries - 1:
                    return None

        logging.error("Failed to complete the request after multiple attempts.")
        return None

    def is_authenticated(self):
        authenticated = self.access_token is not None and time.time() < self.token_expires
        return authenticated

class OpenWeatherAPI:
    def __init__(self, api_key, base_url="https://api.openweathermap.org/data/2.5", units='metric'):
        self.api_key = api_key
        self.base_url = base_url
        self.units = units

    def get_average_daily_temperature(self, latitude, longitude):
        url = f"{self.base_url}/forecast"
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': self.api_key,
            'units': self.units
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            temps = [entry['main']['temp'] for entry in data['list'] if 'main' in entry]
            if not temps:
                logging.warning("No temperature data found.")
                return None
            average_temp = sum(temps) / len(temps)
            logging.info(f"Average temperature calculated successfully for coordinates: {latitude}, {longitude}")
            return average_temp
        except HTTPError as e:
            logging.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except RequestException as e:
            logging.error(f"Request error occurred: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        return None

def get_country_code(country_name):
    import pycountry
    if not country_name:
        logging.error("Country name cannot be empty.")
        raise ValueError("Country name cannot be empty or None.")
    
    try:
        country = pycountry.countries.lookup(country_name)
        country_code = country.alpha_2
        logging.info(f"Country code for {country_name} is {country_code}")
        return country_code
    except LookupError:
        logging.warning(f"Could not find country code for {country_name}. Please check the country name and try again.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while searching for the country code of {country_name}: {str(e)}")
    
    return None

def get_airport_codes(amadeus_api, city_name, country_name=None):
    if not city_name:
        logging.error("City name must be provided.")
        return []

    params = {
        "subType": "AIRPORT",
        "keyword": city_name,
        "sort": "analytics.travelers.score",
        "view": "LIGHT"
    }

    if country_name:
        try:
            country_code = get_country_code(country_name)
            if country_code:
                params["countryCode"] = country_code
            else:
                logging.warning(f"Country code not found for {country_name}; proceeding without country filter.")
        except ValueError as e:
            logging.error(f"Invalid country name provided: {e}")
            return []

    url = f"{amadeus_api.base_url}/reference-data/locations"

    try:
        response_data = amadeus_api.request_with_retry(url, params=params)
        if response_data and 'data' in response_data:
            airports = [item['iataCode'] for item in response_data['data'] if 'iataCode' in item]
            if airports:
                logging.info(f"Airport codes for {city_name}" + (f" in {country_name}" if country_name else "") + f": {airports}")
                return airports
            else:
                logging.warning(f"No airports found matching city '{city_name}'" + (f" in {country_name}" if country_name else "") + ".")
                return []
        else:
            logging.error("Failed to retrieve data or no data found.")
            return []
    except Exception as e:
        logging.error(f"An unexpected error occurred while retrieving airport codes: {str(e)}")
        return []

def get_city_codes(amadeus_api, city_name, country_name=None):
    if not city_name:
        logging.error("City name must be provided.")
        return []

    params = {
        "subType": "CITY",
        "keyword": city_name,
        "view": "FULL"
    }

    if country_name:
        try:
            country_code = get_country_code(country_name)
            if country_code:
                params["countryCode"] = country_code
            else:
                logging.warning(f"Country code not found for {country_name}. Proceeding without country filter.")
        except ValueError as e:
            logging.error(f"Invalid country name provided: {e}")
            return []

    url = f"{amadeus_api.base_url}/reference-data/locations"

    try:
        response_data = amadeus_api.request_with_retry(url, params=params)
        if response_data and 'data' in response_data:
            city_codes = [item['iataCode'] for item in response_data['data'] if 'iataCode' in item]
            if city_codes:
                logging.info(f"City codes for {city_name}: {city_codes}")
                return city_codes
            else:
                logging.warning(f"No city codes found for {city_name}.")
                return []
        else:
            logging.error("Failed to retrieve data or no data found.")
            return []
    except Exception as e:
        logging.error(f"An unexpected error occurred while retrieving city codes: {str(e)}")
        return []

def get_iata_codes(amadeus_api, city_name, country_name=None):
    if not city_name:
        logging.error("City name must be provided.")
        return []

    city_codes = get_city_codes(amadeus_api, city_name, country_name)
    airport_codes = get_airport_codes(amadeus_api, city_name, country_name)

    combined_codes = sorted(set(city_codes + airport_codes))
    
    if combined_codes:
        logging.info(f"Combined IATA codes for {city_name}: {combined_codes}")
    else:
        logging.warning(f"No IATA codes found for {city_name}.")
    
    return combined_codes

def fetch_flight_data_batch(api_instance, origins, departure_date, one_way=False, duration=None, non_stop=False, max_price=None, view_by="DURATION"):
    def fetch_flight_data(origin):
        if not api_instance.is_authenticated():
            logging.info("Attempting to re-authenticate as the current session is not valid or has expired.")
            if not api_instance.authenticate():
                logging.error("Re-authentication failed.")
                return []

        url = f"{api_instance.base_url}/shopping/flight-destinations"
        params = {
            'origin': origin,
            'departureDate': departure_date,
            'oneWay': one_way,
            'duration': duration,
            'nonStop': non_stop,
            'maxPrice': max_price,
            'viewBy': view_by
        }
        params = {k: v for k, v in params.items() if v is not None}

        for attempt in range(3):
            try:
                flights_data = api_instance.request_with_retry(url, params=params)
                if flights_data and 'data' in flights_data:
                    logging.debug(f"Flight data successfully retrieved for {origin} on {departure_date}.")
                    return flights_data['data']
                else:
                    logging.warning(f"No flight data found for {origin} on {departure_date}.")
                    return []
            except Exception as e:
                logging.error(f"HTTP error on attempt {attempt + 1}: {str(e)} for origin {origin}")
                if attempt < 2:
                    sleep_time = (2 ** attempt) + random.uniform(0, 1)
                    logging.info(f"Retrying for {origin} (attempt {attempt + 1}) after sleeping for {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
        return []

    flights_data = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_origin = {executor.submit(fetch_flight_data, origin): origin for origin in origins}
        for future in as_completed(future_to_origin):
            origin = future_to_origin[future]
            try:
                data = future.result()
                flights_data[origin] = data
            except Exception as e:
                logging.error(f"Exception for origin {origin}: {str(e)}")
                flights_data[origin] = []
    return flights_data

def process_flight_data_batch(api_instance, flights, origin):
    destination_codes = {flight.get('destination') for flight in flights if flight.get('destination')}
    location_details = fetch_location_details_batch(api_instance, destination_codes)

    processed_flights = []
    for flight in flights:
        destination_code = flight.get('destination')
        if not destination_code:
            logging.warning(f"Missing destination data for flight from {origin}")
            continue

        flight_offer_url = adjust_url_query(flight.get('links', {}).get('flightOffers', ''))

        details = location_details.get(destination_code)
        if not details:
            logging.warning(f"Location details not found for {destination_code}")
            continue

        processed_flights.append({
            'type': 'flight-destination',
            'origin': origin,
            'destination': destination_code,
            'departureDate': flight.get('departureDate'),
            'returnDate': flight.get('returnDate'),
            'price': flight.get('price', {}).get('total', "N/A"),
            'flightOffer': flight_offer_url,
            'latitude': details.get('geoCode', {}).get('latitude'),
            'longitude': details.get('geoCode', {}).get('longitude')
        })

    return processed_flights

def find_cheapest_flight_destinations(api_instance, origins, departure_date, one_way=False, duration=None, non_stop=False, max_price=None, view_by='DURATION', limit=None):
    flights_data = fetch_flight_data_batch(api_instance, origins, departure_date, one_way, duration, non_stop, max_price, view_by)

    all_flights = []
    for origin, flights in flights_data.items():
        if flights:
            processed_flights = process_flight_data_batch(api_instance, flights, origin)
            all_flights.extend(processed_flights)
        else:
            logging.warning(f"No flight data available for origin: {origin}")

    if not all_flights:
        logging.info("No valid flights found after processing.")
        return pd.DataFrame()

    flights_df = pd.DataFrame(all_flights)

    if not flights_df.empty:
        flights_df['price'] = pd.to_numeric(flights_df['price'], errors='coerce')
        flights_df.dropna(subset=['price', 'latitude', 'longitude'], inplace=True)
        flights_df.sort_values(by='price', inplace=True)
        flights_df = flights_df.groupby('destination', as_index=False).first()
        flights_df.sort_values(by='price', ascending=True, inplace=True)
        flights_df.reset_index(drop=True, inplace=True)
        if limit:
            flights_df = flights_df.head(limit)
            logging.info(f"Displaying up to {limit} cheapest flights.")
        else:
            logging.info("Displaying all cheapest flights.")
    else:
        logging.info("No valid flights found after processing.")

    return flights_df

def adjust_url_query(url):
    if not url:
        return ""

    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        if 'currency' in query_params:
            query_params['currencyCode'] = query_params.pop('currency')
        
        new_query_string = urlencode(query_params, doseq=True)
        return urlunparse(parsed_url._replace(query=new_query_string))
    except Exception as e:
        logging.error(f"Error adjusting URL query: {str(e)}")
        return ""

def fetch_location_details(api_instance, iata_code):
    if iata_code in location_cache:
        logging.debug(f"Cache hit for {iata_code}")
        return location_cache[iata_code]

    location_detail = attempt_fetch_location(api_instance, f"{api_instance.base_url}/reference-data/locations/cities", {
        'keyword': iata_code,
        'max': 1
    }, iata_code)

    if location_detail:
        return location_detail

    location_detail = attempt_fetch_location(api_instance, f"{api_instance.base_url}/reference-data/locations", {
        'subType': 'AIRPORT,CITY',
        'keyword': iata_code,
        'view': 'FULL'
    }, iata_code)

    if location_detail:
        return location_detail

    logging.warning(f"No location details found for IATA code {iata_code}")
    return None

def fetch_location_details_batch(api_instance, iata_codes):
    location_details = {}

    def fetch_location(iata_code):
        return fetch_location_details(api_instance, iata_code)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_iata_code = {executor.submit(fetch_location, code): code for code in iata_codes}
        for future in as_completed(future_to_iata_code):
            code = future_to_iata_code[future]
            try:
                details = future.result()
                if details:
                    location_details[code] = details
            except Exception as e:
                logging.error(f"Exception for IATA code {code}: {str(e)}")

    return location_details

def filter_flights_by_weather(api_instance, flights_df, temp_min, temp_max):
    logging.info("Filtering flights based on weather conditions.")
    filtered_flights = []

    def get_filtered_row(row):
        try:
            avg_temp = api_instance.get_average_daily_temperature(row['latitude'], row['longitude'])
            if avg_temp is None:
                logging.warning(f"Weather data not available for coordinates ({row['latitude']}, {row['longitude']}). Skipping.")
                return None
            if temp_min <= avg_temp <= temp_max:
                row['Average Temperature'] = avg_temp
                return row
        except Exception as e:
            logging.error(f"Error retrieving weather data for {row['destination']}: {e}")
        return None

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_filtered_row, row) for _, row in flights_df.iterrows()]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                filtered_flights.append(result)

    if not filtered_flights:
        logging.info("No flights found within the specified temperature range.")
        return pd.DataFrame()

    result_df = pd.DataFrame(filtered_flights)
    result_df.sort_values(by='price', ascending=True, inplace=True)
    result_df.reset_index(drop=True, inplace=True)
    return result_df

def suche_fluege():
    st.title('Flüge suchen')
    st.write("Geben Sie Ihre Suchkriterien ein, um verfügbare Flüge zu finden.")
    abflugort = st.text_input("Abflughafen:", "Frankfurt")
    min_temperatur = st.number_input("Minimale Zieltemperatur:", value=10)
    max_temperatur = st.number_input("Maximale Zieltemperatur:", value=25)
    departure_date = st.text_input("Abflugdatum (YYYY-MM-DD):", "2024-06-01")

    if st.button("Flüge suchen"):
        amadeus_api = AmadeusAPI(AMADEUS_API_KEY, AMADEUS_API_SECRET, AMADEUS_API_URLs['base_url'])
        weather_api = OpenWeatherAPI(OPEN_WEATHER_API_KEY)

        if not amadeus_api.authenticate():
            st.error("Authentifizierung mit der Amadeus API fehlgeschlagen.")
            return

        iata_codes = get_iata_codes(amadeus_api, abflugort)
        if not iata_codes:
            st.error(f"Keine IATA-Codes für den angegebenen Abflughafen {abflugort} gefunden.")
            return

        flights_df = find_cheapest_flight_destinations(
            amadeus_api, iata_codes, departure_date, one_way=False, duration="1,10", non_stop=False, max_price=1000, view_by="DURATION"
        )

        if flights_df.empty:
            st.write("Keine Flüge gefunden.")
            return

        filtered_flights_df = filter_flights_by_weather(weather_api, flights_df, min_temperatur, max_temperatur)
        if filtered_flights_df.empty:
            st.write("Keine Flüge gefunden, die die Temperaturkriterien erfüllen.")
        else:
            st.write("Verfügbare Flüge:")
            df = filtered_flights_df.rename(columns={
                "destination": "Zielort",
                "departureDate": "Abflugdatum",
                "returnDate": "Rückkehrdatum",
                "price": "Preis (€)",
                "Average Temperature": "Durchschnittstemperatur (°C)"
            })
            df["Preis (€)"] = df["Preis (€)"].round(2)
            df["Durchschnittstemperatur (°C)"] = df["Durchschnittstemperatur (°C)"].round(2)
            st.dataframe(df.sort_values(by=["Preis (€)"], ascending=True))


# Fetch Weather Data
def fetch_weather_data(city):
    api_key = "Jr69lfgFLTikdM27"
    lat, lon = get_lat_lon(city, api_key)
    url = f"https://my.meteoblue.com/packages/basic-day?apikey={api_key}&lat={lat}&lon={lon}&asl=279&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data_day']
        df = pd.DataFrame({
            'Datum': pd.to_datetime(data['time']),
            'Temperatur (°C)': data['temperature_mean'],
            'Niederschlag (mm)': data['precipitation']
        })
        return df.iloc[:5]  # Limit to next 5 days
    else:
        st.error("Failed to fetch weather data.")
        return pd.DataFrame()

def plot_weather_data(df):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Datum')
    ax1.set_ylabel('Temperatur (°C)', color=color)
    ax1.plot(df['Datum'], df['Temperatur (°C)'], color=color, marker='o', linestyle='-', linewidth=2, markersize=5, zorder=3)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Niederschlag (mm)', color=color)
    ax2.plot(df['Datum'], df['Niederschlag (mm)'], color=color, marker='o', linestyle='-', linewidth=2, markersize=5, zorder=2)
    ax2.fill_between(df['Datum'], 0, df['Niederschlag (mm)'], facecolor=color, alpha=0.3, hatch='//', zorder=2)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(bottom=0)

    plt.title('Wettervorhersage für die nächsten 5 Tage')
    plt.tight_layout()
    st.pyplot(fig)

def get_lat_lon(city, api_key):
    url = f"https://www.meteoblue.com/en/server/search/query3?query={city}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            first_result = data['results'][0]
            return first_result['lat'], first_result['lon']
        else:
            st.error("No results found for the specified location.")
            return None, None
    else:
        st.error("Failed to fetch coordinates. Please check your API key and network connection.")
        return None, None

def temperaturkarte():
    st.title('Wettervorhersage-Dashboard')
    city = st.text_input("Stadt eingeben:", "Basel")
    
    if st.button('Wettervorhersage anzeigen'):
        df = fetch_weather_data(city)
        plot_weather_data(df)

def generate_packliste_items(temperature, weather):
    kleidung = []
    kulturbeutel = ["Zahnbürste", "Zahnpasta", "Deo", "Shampoo", "Seife", "Sonnencreme"]
    dokumente = ["Reisepass", "Visum", "Kreditkarten", "Bargeld", "Versicherungsdokumente", "Reiseplan"]

    if temperature < 10:
        kleidung.extend(["Warme Jacke", "Handschuhe", "Mütze", "Schal", "Thermounterwäsche"])
        if weather == "Schnee":
            kleidung.extend(["Schneeschuhe", "Wasserdichte Hose"])
    elif 10 <= temperature <= 20:
        kleidung.extend(["Leichte Jacke", "Pullover", "Lange Hosen"])
        if weather == "Regen":
            kleidung.extend(["Regenjacke", "Regenschirm"])
    else:
        kleidung.extend(["T-Shirts", "Shorts", "Flip-Flops"])
        if weather == "Sonnig":
            kleidung.extend(["Sonnenbrille", "Sonnenhut"])

    return kleidung, kulturbeutel, dokumente

def packliste():
    st.title("Packliste")

    temperatur = st.number_input("Wie hoch ist die Temperatur an deinem Zielort?", format='%d', step=1)
    wetter_optionen = ["Sonnig", "Regen", "Schnee", "Bewölkt"]
    wetter = st.selectbox("Wähle die Wetterverhältnisse aus", wetter_optionen)
    generate_button = st.button("Packliste anzeigen")

    if 'init' not in st.session_state:
        st.session_state['init'] = True
        st.session_state['checkliste_erzeugt'] = False
        st.session_state['items_checked'] = {}

    if generate_button:
        st.session_state['temperatur'] = temperatur
        st.session_state['wetter'] = wetter
        st.session_state['checkliste_erzeugt'] = True

    if st.session_state['checkliste_erzeugt']:
        temperatur = st.session_state['temperatur']
        wetter = st.session_state['wetter']

        kleidung, kulturbeutel, dokumente = generate_packliste_items(temperatur, wetter)

        kategorien = {
            "Kleidung": kleidung,
            "Kulturbeutel": kulturbeutel,
            "Dokumente": dokumente
        }

        for kategorie, inhalte in kategorien.items():
            st.subheader(kategorie)
            for artikel in inhalte:
                checkbox_id = f"checkbox_{artikel}_{kategorie}"
                
                if checkbox_id not in st.session_state['items_checked']:
                    st.session_state['items_checked'][checkbox_id] = False

                col1, col2 = st.columns([1, 4])
                with col1:
                    checked = st.checkbox("", key=checkbox_id, value=st.session_state['items_checked'][checkbox_id])
                st.session_state['items_checked'][checkbox_id] = checked

                with col2:
                    if checked:
                        st.markdown(f"<span style='text-decoration: line-through;'>{artikel}</span>", unsafe_allow_html=True)
                    else:
                        st.write(artikel)

def main():
    load_css()
    st.sidebar.title("Menü")
    app_modus = st.sidebar.selectbox("Wähle eine Option", ["Flüge suchen", "Temperaturkarte anzeigen", "Packliste"])

    if app_modus == "Flüge suchen":
        suche_fluege()
    elif app_modus == "Temperaturkarte anzeigen":
        temperaturkarte()
    elif app_modus == "Packliste":
        packliste()

if __name__ == "__main__":
    main()

import requests

url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

querystring = {"fromId":"BOM.AIRPORT","toId":"DEL.AIRPORT","departDate":"<REQUIRED>","pageNo":"1","adults":"1","children":"0,17","currency_code":"AED"}

headers = {
	"X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
	"X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
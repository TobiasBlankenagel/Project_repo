import requests

url = "https://travel-advisor.p.rapidapi.com/airports/search"

querystring = {"query":"new york","locale":"en_US"}

headers = {
	"X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
	"X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
import requests

url = "https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete"

querystring = {"query":"new","market":"US","locale":"en-US"}

headers = {
	"X-RapidAPI-Key": "20c5e19a55msh027a6942760467ap12650bjsne0765678bd0a",
	"X-RapidAPI-Host": "skyscanner80.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
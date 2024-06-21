
import json
import requests

def test_api ():
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London%2CUK?unitGroup=us&key=H82G8KM7VFWSPUHDYJ49E7VBH"
    response = requests.get(url)

    print(response.status_code)
    print(response.json())

    address = response.json()['address']
    day = response.json()['days'][0]['temp']
    pressure = response.json()['days'][1]['pressure']
    print(address)
    print(day)
    print(pressure)

test_api()
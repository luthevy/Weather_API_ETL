""" 
    This source is used for crawling data from OpenWeather API and write to JSON file
"""
from asyncio.windows_events import NULL
import requests
import os

def progress(status, remaining, total):
    """ 
    Display progress of copying database page
    :param: str response : data from API
            str file_name: name of JSON file
    :return: new JSON file filled with weather data
    """
    print(f'Copied {total - remaining} of {total} pages...')
    
def write_json(response,file_name):
    """ 
    Save data from API into JSON file
    :param: str response : data from API
            str file_name: name of JSON file
    :return: new JSON file filled with weather data
    """
    disallowed_characters = "()test[]"
    tmp = response
    # Remove specific characters in response string (which has form "test(<data_in_json_format>)")
    for character in disallowed_characters:
        tmp = tmp.replace(character, "")
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(tmp)
            print("Saving data successfully!")
    except:
        print("An exception occurred!")
	

def crawl_data(loc,unit,file_name):
    """ Crawl data from API process
    Based on given location and unit type, crawl weather data of that location

    :param: str loc : name of city
            str unit: unit type, metric or imperial
            str file_name : name of JSON file
    :return: new JSON file filled with weather data
    """
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"q":loc,"lat":"0","lon":"0","callback":"test","id":"2172797","lang":"en","units":unit,"mode":"xml"}
    headers = {
		"X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
		"X-RapidAPI-Key": "fe2fdce76emsh9ba685183b38824p19c726jsn087604409efc"
	}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        write_json(response.text,file_name)
    except:
        print('City not found! Type again or try another')

def get_repo():
    """
    Display current working repository (to display hidden database location)
    """
    print(os.getcwd())
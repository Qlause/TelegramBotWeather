import requests

TOKEN = ""

class Weather:
    def __init__(self, lat, lon, appid = TOKEN, exclude = ["minutely", "daily"], units = "metric", lang="en"):
        self.lat = lat
        self.lon = lon
        self.exclude = exclude
        self.unit = units
        self.appid = appid
        self.lang = lang
        
        self.params = {
                    "lat": self.lat,
                    "lon": self.lon,
                    "exclude":self.exclude,
                    "units":self.unit,
                    "lang": self.lang,
                    "appid":self.appid
                        }
    
    def call_api(self):
        return requests.get("https://api.openweathermap.org/data/2.5/onecall", params=self.params)
    
    def get_now(self):
        self.exclude = ["minutely","hourly", "daily"]   
        return self.call_api().json()["current"]

    def get_data(self, data="hourly"):
        exclude = ["minutely", "hourly", "current", "current", "daily"]  
        exclude.remove(data)
        self.exclude = exclude
        
        return self.call_api().json()
        

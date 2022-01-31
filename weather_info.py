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
    
    def get_hourly(self, interval=6):
        self.exclude = ["minutely", "daily"]
        
        res = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=self.params)
        data = res.json()["hourly"][interval - 1]
        
        return data
        

weather = Weather(lat=37.807343, lon=126.713508)    
print(weather.get_hourly()["temp"])
        
        
        
        
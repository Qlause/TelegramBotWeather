from weather_info import Weather
from message_generator import Message

class PredictWeather:
    def __init__(self, wt: Weather, data="hourly"):
        self.weather = wt
        self.selected = data
        self.data = self.weather.get_data(self.selected)
    
    def current_weather(self):
        pass
    
    def predict_one_day(self):
        rain_data = False
        if self.rain_predict() != False:
            rain_data =  self.rain_predict()
        
        sunny_data = False
        if self.sunny_predict() != False:
            sunny_data =  self.sunny_predict()
        
        all_data = {"rain":rain_data, 
                    "sunny":sunny_data}
        
        snow_data = False
        if self.snow_predict() != False:
            snow_data = self.snow_predict()
        
        all_data = {"rain":rain_data, 
                    "sunny":sunny_data,
                    "snow":snow_data}
        
        temp = {"rain" : False,
                "sunny": False,
                "snow":False,
                "rain_at": None,
                "snow_at": None,
                "realtemp": [None,None],
                "feeltemp": [None,None],
                "cur_wet":False,
                "cur_temp":False,
                "cur_feel":False}
        
        if all_data["rain"] != False:
            temp["rain"] = True
            temp["rain_at"] = all_data["rain"][0]["at"]
            
            for rain in all_data["rain"]:
                if temp["realtemp"][0] == None: 
                    temp["realtemp"][1] = rain["temp"] 
                    temp["realtemp"][0] = rain["temp"] 
            
                if temp["feeltemp"][0] == None: 
                    temp["feeltemp"][0] = rain["feels_like"]
                    temp["feeltemp"][1] = rain["feels_like"]
                
                elif rain["temp"] > temp["realtemp"][1]:
                    temp["realtemp"][1] = rain["temp"]
                elif rain["temp"] < temp["realtemp"][0]:
                    temp["realtemp"][0] = rain["temp"]
                      
                if rain["feels_like"] > temp["feeltemp"][1]: 
                    temp["feeltemp"][1] = rain["feels_like"]
                elif rain["feels_like"] < temp["feeltemp"][0]:
                    temp["feeltemp"][0] = rain["feels_like"]
        
        if all_data["snow"] != False:
            temp["snow"] = True
            temp["snow_at"] = all_data["snow"][0]["at"]
            
            for snow in all_data["snow"]:
                
                if temp["realtemp"][0] == None: 
                    temp["realtemp"][1] = snow["temp"] 
                    temp["realtemp"][0] = snow["temp"] 
            
                if temp["feeltemp"][0] == 0: 
                    temp["feeltemp"][0] = snow["feels_like"]
                    temp["feeltemp"][1] = snow["feels_like"]

                if  snow["temp"] > temp["realtemp"][1]: 
                    temp["realtemp"][1] = snow["temp"]
                elif snow["temp"] < temp["realtemp"][0]:
                    temp["realtemp"][0] = snow["temp"]

                if snow["feels_like"] > temp["feeltemp"][1]: 
                    temp["feeltemp"][1] = snow["feels_like"]
                elif snow["feels_like"] < temp["feeltemp"][0]:
                    temp["feeltemp"][0] = snow["feels_like"]

        if all_data["sunny"] != False:
            temp["sunny"] = True
            
            for sun in all_data["sunny"]:
                if temp["realtemp"][0] == None: 
                    temp["realtemp"][1] = sun["temp"] 
                    temp["realtemp"][0] = sun["temp"] 
            
                if temp["feeltemp"][0] == None: 
                    temp["feeltemp"][0] = sun["feels_like"]
                    temp["feeltemp"][1] = sun["feels_like"]

                if  sun["temp"] > temp["realtemp"][1]: 
                    temp["realtemp"][1] = sun["temp"]
                elif sun["temp"] < temp["realtemp"][0]:
                    temp["realtemp"][0] = sun["temp"]

                if sun["feels_like"] > temp["feeltemp"][1]: 
                    temp["feeltemp"][1] = sun["feels_like"]
                elif sun["feels_like"] < temp["feeltemp"][0]:
                    temp["feeltemp"][0] = sun["feels_like"]
        
        return temp
    
    def cur_data(self):
        data = self.weather.get_now()
        
        main = data["weather"][0]["main"]
        temp = data["temp"]
        feels_temp = data["feels_like"]
        
        return main, temp, feels_temp
    
    
        
    def rain_predict(self):      
        rain = []
        for index, data in enumerate(self.data[self.selected][:11]):
            if data["weather"][0]["id"] < 600:
                rain.append({"id": data["weather"][0]["id"],
                            "at": index + 1,
                            "temp":  data["temp"],
                            "feels_like":  data["feels_like"],
                            "main": data["weather"][0]["main"], 
                            "des":data["weather"][0]["description"]})
        
        if len(rain) >= 1:
            return rain
        
        return False
    
    def snow_predict(self):      
        snow = []
        for index, data in enumerate(self.data[self.selected][:11]):
            if  600 < data["weather"][0]["id"] < 700:
                snow.append({"id": data["weather"][0]["id"],
                            "at": index + 1,
                            "temp":  data["temp"],
                            "feels_like":  data["feels_like"],
                            "main": data["weather"][0]["main"], 
                            "des":data["weather"][0]["description"]})
        
        if len(snow) >= 1:
            return snow
        
        return False

    def sunny_predict(self):
        sunny = []
        for index, data in enumerate(self.data[self.selected][:11]):
            if data["weather"][0]["id"] > 700:
                sunny.append({"id": data["weather"][0]["id"],
                            "at": index + 1,
                            "temp":  data["temp"],
                            "feels_like":  data["feels_like"],
                            "main": data["weather"][0]["main"], 
                            "des":data["weather"][0]["description"]})
        
        if len(sunny) >= 1:
            return sunny
        
        return False
    
import emoji
import math
import random
from weather_info import Weather

class Message:
    def __init__(self, **kw):
        self.sunny = kw.get("sunny", False)
        self.rain = kw.get("rain", False)
        self.rain_at = kw.get("rain_at", None)
        self.snow = kw.get("snow", False)
        self.snow_at = kw.get("snow_at", None)
        self.realtemp = kw.get("realtemp", [0,0])
        self.feeltemp = kw.get("feeltemp", [0,0])
        
    
    def generate_predict_message(self):
        heart = emoji.emojize(":red_heart:")
        return f"""QLAUSE WEATHER BOT\nMade with {heart}\n==========================\nInfo for next 12 Hours :\n\n{self.sunnym()}\n\n{self.rainm()}\n\n{self.snowm()}\n\n{self.tempm()}."""
    
    def author_message(self):
        listmsg = []
        with open("msg.txt", "r") as msg:
            for msgs in msg:
                listmsg.append(msgs.strip())
        
        return random.choice(listmsg)
    
    def sunnym(self):
        sun = emoji.emojize(":sun_behind_cloud:")
        cloud = emoji.emojize(":cloud:")
        sun_x = emoji.emojize(":cross_mark:")
        if self.sunny != False:
            return f"Sunny and Cloudy,{sun}{cloud}"
        return f"Sun won't appear this day,{sun}{sun_x}"
    
    def rainm(self):
        rain = emoji.emojize(":cloud_with_rain:")
        umb = emoji.emojize(":umbrella_with_rain_drops:")
        rain_x = emoji.emojize(":cross_mark:")
        rain_4 = emoji.emojize(":one_o’clock:")
        rain_1 = emoji.emojize(":two_o’clock:")
        rain_2 = emoji.emojize(":three_o’clock:")
        rain_3 = emoji.emojize(":four_o’clock:")

        if self.rain != False:
            return f"Rain will come ~{self.rain_at} Hours From now,{rain_1}{rain_3}{rain_4}{rain_2}\nPlease Take your Umbrella,{rain}{umb}"
        return f"No Rain, \nYou dont have to bring umbrella,{rain}{rain_x}"
    
    def snowm(self):
        snow = emoji.emojize(":snowflake:")
        snow_x = emoji.emojize(":cross_mark:")
        if self.snow != False:
            return f"Rain will come {self.snow_at} Hours From now, be carefull{snow}"
        return f"No Snow,{snow}{snow_x}"
        
    def tempm(self):
        highest = math.ceil(self.realtemp[1]) 
        lowest = math.ceil(self.realtemp[0])
        
        highest_feel = math.ceil(self.feeltemp[1]) 
        lowest_feel = math.ceil(self.feeltemp[0])
        msg = f"Temperature will be around {lowest}C ~ {highest}C\nBut it'll feel like {lowest_feel}C ~ {highest_feel}C "
        
        fire = emoji.emojize(":fire:")
        hot = emoji.emojize(":hot_face:")
        ok = emoji.emojize(":smiling_face_with_sunglasses:")
        cold = emoji.emojize(":cold_face:")
        
        wea = None
        if highest_feel >= 32:
            wea = f"{fire}{hot}" * 4
        elif 29 <= highest_feel <= 31:
            wea = f"{hot}" * 4
        elif 24 <= highest_feel <= 28:
            wea = f"{ok}" * 4
        elif 18 <= highest_feel <= 23:
            wea = f"{cold}" * 2
        elif highest_feel <= 17:
            wea = f"{cold}" * 5
        
        return msg + wea
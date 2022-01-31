from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater
import time 
import threading
from weather_info import Weather

TOKEN = "5115237864:AAHGSChjEBtps3pBTcHvgNCcrJJ3ww2BPfs"
is_continue = True
start_threading = None
stop_threading = None

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def welcome(update: Update, context: CallbackContext):
   update.message.reply_text(f"""Bot Has Started\n\n /start_weather (lat) (long) : to start\n /stop_weather: to stop bot""")

def start_bot(update: Update, context: CallbackContext):
    global is_continue
    
    lat = context.args[0]
    long = context.args[1]   
        
    while is_continue == True:
        weather = Weather(lat=lat, lon=long, lang="id")

        weather_info = weather.get_hourly()["weather"][0]["description"]
        temp_info = weather.get_hourly()["temp"]
        
        update.message.reply_text(f"6 Jam Kedepan {weather_info}\n Dengan Temperature {temp_info}C")
        time.sleep(3600)

def stop_bot(update: Update, context: CallbackContext):
    global is_continue
        
    is_continue = False
    update.message.reply_text(f"stopped!")
    
def start(update: Update, context: CallbackContext):
    global start_threading, stop_threading
    
    start_threading = threading.Thread(target=start_bot, args=(update, context))
    stop_threading = threading.Thread(target=stop_bot, args=(update, context))
    
    start_threading.start()
    
def stop(update: Update, context: CallbackContext):
    global start_threading, stop_threading
    
    stop_threading.start()
    
    start_threading.join()
    stop_threading.join()
    
start_handler = CommandHandler('start', welcome)
dispatcher.add_handler(start_handler)

start_weather_handler = CommandHandler('start_weather', start)
dispatcher.add_handler(start_weather_handler)

stop_weather_handler = CommandHandler('stop_weather', stop)
dispatcher.add_handler(stop_weather_handler)

updater.start_polling()
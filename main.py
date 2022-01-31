from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater
import time
import threading
from weather_info import Weather

TOKEN = ""
start_threading = {}
stop_threading = {}

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def welcome(update: Update, context: CallbackContext):
   update.message.reply_text(f"""Bot Has Started\n\n /start_weather (lat) (long) : to start\n /stop_weather: to stop bot""")

def start_bot(update: Update, context: CallbackContext):

    lat = context.args[0]
    long = context.args[1]
    user_id = context._user_id_and_data[0]

    while start_threading[user_id][1] == True:

        weather = Weather(lat=lat, lon=long, lang="id")

        cur_temp = weather.get_now()["temp"]
        cur_temp_f = weather.get_now()["feels_like"]
        cur_weather = weather.get_now()["weather"][0]["main"]
        weather_info = weather.get_hourly()["weather"][0]["main"]
        temp_info = weather.get_hourly()["temp"]

        update.message.reply_text(f"Cuaca Saat ini : {cur_weather}, {cur_temp}C (Terasa Seperti {cur_temp_f}C)\n\n6 Jam Kedepan : {weather_info}\nDengan Temperature : {temp_info}C\n\nNext Update in 1 Hour")
        
        for _ in range(0,4):
            if start_threading[user_id][1] == False:
                break
            time.sleep(1)

    start_threading[user_id][1] = True

def stop_bot(update: Update, context: CallbackContext):

    user_id = context._user_id_and_data[0]

    start_threading[user_id][1] = False
    update.message.reply_text(f"stopped!")

def start(update: Update, context: CallbackContext):
    global start_threading, stop_threading

    user_id = context._user_id_and_data[0]

    if user_id in start_threading:
        start_threading[user_id][1] = False
        start_threading[user_id][0].join()
        start_threading.pop(user_id)
        
    new_thread = threading.Thread(target=start_bot, args=(update, context))
    new_stop_threading = threading.Thread(target=stop_bot, args=(update, context))

    start_threading[user_id] = [new_thread, True]
    stop_threading[user_id] = new_stop_threading

    start_threading[user_id][0].start()

def stop(update: Update, context: CallbackContext):
    global stop_threading

    user_id = context._user_id_and_data[0]
    stop_threading[user_id].start()
    stop_threading[user_id].join()
    start_threading[user_id][0].join()

def printdata(update: Update, context: CallbackContext):
    global start_threading
    update.message.reply_text(str(start_threading))

start_handler = CommandHandler('start', welcome)
dispatcher.add_handler(start_handler)

start_weather_handler = CommandHandler('start_weather', start)
dispatcher.add_handler(start_weather_handler)

stop_weather_handler = CommandHandler('stop_weather', stop)
dispatcher.add_handler(stop_weather_handler)

printdata = CommandHandler('print', printdata)
dispatcher.add_handler(printdata)

updater.start_polling()

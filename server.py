from bot import telegram_chatbot
from hx711 import HX711
import RPi.GPIO as GPIO
import configparser
import datetime
import sys

#Bot setup
update_id = None
config = "config.ini"
bot = telegram_chatbot(config)

#Parser setup
parser = configparser.SafeConfigParser()

#Scale setup
hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(1509)
hx.reset()
hx.tare()

#Cleanup
def cleanAndExit():
    GPIO.cleanup()
    sys.exit()

#Scale reset
def scale_reset(config):
    parser.read(config)
    parser.set('creds', 'weight', '0')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    hx.reset()
    hx.tare()

#Scale calibration
def scale_calibrate(config, val):
    val = str(val)
    parser.read(config)
    parser.set('creds', 'weight', val)
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)

def get_pot_weight(config):
    parser.read(config)
    val = parser.getint('creds', 'weight')
    return val

#Making the reply message according to user message
def make_reply(msg):
    if msg is not None:
        dl = 0
        cups = 0
        pot_weight = get_pot_weight(config)
        val = max(0, int(hx.get_weight(5))) - pot_weight
        if val < 0:
            val = 0
        elif val > 0:
            dl = val / 100.00
            cups = dl / 2
        date = datetime.datetime.now()
        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%y")
        hour = date.strftime("%H")
        minute = date.strftime("%M")
        timestamp = "[{}/{}/{} {}:{}]".format(day, month, year, hour, minute)
        if val < 0:
            reply = "{}\nError. Value of scale information is below zero. Contact the administrator {}.".format(timestamp)

        elif msg == "/start" or msg == "/help":
            reply = """{}\nThe basic commands for the bot are:\n /coffee --> Tells you how much coffee there is.\n /help --> Shows you this message
/reset --> Resets the scale\n/calibrate --> Calibrates the scale\n/calibhelp --> Help on calibration""".format(timestamp)

        elif msg == "/reset":
            scale_reset(config)
            reply = "{}\nReset done. You have to redo the calibration for the scale. Information on how to do the calibration type command /calibhelp".format(timestamp)

        elif msg == "/calibrate":
            scale_calibrate(config, val)
            reply = "{}\nCalibration done. The weight of the pot is {} grams".format(timestamp, val)

        elif msg == "/calibhelp":
            reply = """{}\nTo calibrate the scale, first send the /reset command to the bot and then place an empty pot on the scale.
After this send the /calibrate message to the bot. After this the calibration is done""".format(timestamp)

        elif msg == "/coffee":
            if cups <= 0:
                reply = "{}\nThere is no coffee in the pot, or the scale system needs a reset. Go check the situation!".format(timestamp)
            elif cups > 0:
                reply = "{}\nThere is approximately {} cups of coffee in the pot ({}dl)".format(timestamp, cups, dl)

        elif msg != "/coffee" and msg != "/start" and msg != "/help" and msg != "/reset" and msg != "/calibhelp":
            reply = "{}\nNot a valid command. Use command /help to see all available commands".format(timestamp)
        #elif msg == "/sub":
            #TODO: Subscribe system to get a notification when there is fresh coffee brewing
    elif msg == None:
        reply = "{}\nYour message appeared to be empty or incorrect. Please try again. (use command /help for available commands)".format(timestamp)
    return reply

#Infinite loop to run the bot while the pi is on
while True:
    try:
        print "..."
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                try:
                    message = item["message"]["text"]
                except:
                    message = None
                from_ = item["message"]["from"]["id"]
                reply = make_reply(message)
                bot.send_message(reply, from_)
    except(KeyboardInterrupt, SystemExit):
        cleanAndExit()

#
# Sample to send Whatsapp Messages through IBM Cloud Function
# The original use case was that of sending reminders to my mother for her pills but can easily be adapted to many other use cases
#
# This code only sends messages, it does not check that the message was read by the reciever (but this can be done through 
# the Twilio APIs: https://www.twilio.com/docs/whatsapp/api#monitor-the-status-of-your-whatsapp-outbound-message)
# 
# main() will be run when you invoke this action ni IBM Cloud Function (rund exactly the same as open source Apache OpenWhisk)
#
# **args is a dictionary of parameters that we will bind to the "package" where this action resides. The "package" is just a way a way to
# wrap up several objects in a single entity
#
# Download the helper library from https://www.twilio.com/docs/python/install
# The Account Sid and Auth Token from twilio.com/console which tou should have prepared beforehand
# 
# if main called with 0 argument main(0) then will read the parms from the local file
#
# Author: Enric Delgado Samper, during Coronavirus crisis to help my mom 
# 


from twilio.rest import Client
import sys
from datetime import datetime
import pytz


def main(args):

# Only for local testing purposes:
    if (args == 0):
        import ast 
        file = open("parmsPackage.json", "r")
        contents = file.read()
        parms = ast.literal_eval(contents)
        print(parms)
    else:
        parms=args

    account_sid = parms["AccountID"]
    auth_token = parms["AuthToken"]
    telefon_send = parms["TlfSender"]
    telefon_receive = parms["TlfReceiver"]
    Message_Breakfast = parms["MessageBreakfast"]
    Message_Lunch = parms["MessageLunch"]
    Message_Dinner = parms["MessageDinner"]

    client = Client(account_sid, auth_token)

# We set the right timezone and extract current hour to display the message accordinglky

    tz = pytz.timezone('Europe/Berlin')
    Barcelona_now = datetime.now(tz).strftime('%d-%b-%Y (%H:%M:%S)') 
    Barcelona_now_Hour = datetime.now(tz).hour

    if (Barcelona_now_Hour) in range(7,11):      # Breakfast time
        miss = Message_Breakfast
    elif (Barcelona_now_Hour) in range(12, 16):  # Lunch time
        miss = Message_Lunch
    elif (Barcelona_now_Hour) in range(20, 24):  # Dinner time
        miss = Message_Dinner
    else:
         miss = "Cap pastilla ara"

# We send the message

    message = client.messages.create(
                            body = Barcelona_now + '\n' + miss,
                            from_='whatsapp:' + telefon_send,
                            to='whatsapp:' + telefon_receive
                          )

    return { 'message': message.sid }



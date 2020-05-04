import pyttsx3 #gtts
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import game as ga
import random
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

# print(voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing!")
        query = r.recognize_google(audio, language='en-in')
        print("User said : ", query)
    except Exception as e:
        print(e)
        print("Say again")
        speak("Sorry! , Say again")
        takecommand()
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('yourmail@gmail.com', 'your password')
    fromaddr = "yourmail@gmail.com"
    toaddr = to  
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Donot reply"
    body = content
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server.sendmail('yourmail@gmail.com', toaddr, text)
    server.close()

def network_finder(number):

    ch_number=phonenumbers.parse(number,'CH')
    # CH -> Country History or Information or belongs
    # RO -> Register Organisation (Your phone belongs to which network) 
    print(geocoder.description_for_number(ch_number,"en"))

    service_nmber = phonenumbers.parse(number,"RO")
    print(carrier.name_for_number(service_nmber,"en"))
    speak(carrier.name_for_number(service_nmber,"en"))

def weather(city):
    # Pass your API key here 
    api_key = "42cb1988227c341dba6029164a2a1ddb"

    
    ow_url = "http://api.openweathermap.org/data/2.5/forecast?"
    with open ('city.list.json',encoding="utf8") as f:
        data = f.read()

    obj = json.loads(data)    
    for j in range(0,len(obj)):
        if obj[j]['name'].lower() == city.lower() :
            id = obj[j]['id']

    call_url = ow_url +"id="+str(id)+"&APPID="+api_key

    # Fire a GET request to API 
    response = requests.get(call_url) 

    # fetch data from JSON response
    data = response.json()

    if data["cod"] != "404": 
    
        
        city_res = data['list'][1]
        current_temperature = city_res['main']['temp']
        current_temperature = current_temperature - 273.15
        print("Temperature is : ", current_temperature)
        speak("Temperature is : ")
        speak(current_temperature)
    else: 
        print(" City Not Found ") 

def msg(to, content):

    URL = 'https://www.sms4india.com/api/v1/sendCampaign'

    # get request
    def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
        req_params = {
        'apikey':apiKey,
        'secret':secretKey,
        'usetype':useType,
        'phone': phoneNo,
        'message':textMessage,
        'senderid':senderId
        }
        return requests.post(reqUrl, req_params)

    # get response
    response = sendPostRequest(URL, 'SDVORHVZRVVOGLHQBTZWY2M1PFV4B7J2', '1M7ZUWLRWUBX2J6X', 'stage', to, 'kaushiktom@gmail.com', content )
    """
    Note:-
        you must provide apikey, secretkey, usetype, mobile, senderid and message values
        and then requst to api
    """
    # print response if you want
    res = json.loads(response.text)
    print(res["status"])
    speak(res["status"])


def set_path(i):
    switcher = {
        1:'C:\\',
        2:'D:\\',
        3:'E:\\',
        4:'C:\\Users\\Sekhar\\Pictures',
        5:'C:\\Users\\Sekhar\\Downloads',
        6:'C:\\Users\\Sekhar\\Music',
        7:'C:\\Users\\Sekhar\\Videos'
    }
    return switcher.get(i,"nothing")

def welcome():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")
    elif hour>=18 and hour<=23:
        speak("Good Evening Sir!")
    
    speak("I am JARVIS. How can i help you Sir ?")

def process_query(command):
    try:
        if "who are you" in command or "define yourself" in command:
            content = '''Hello, I am Your personal Assistant. 
            I am here to make your life easier. You can command me to perform 
            various tasks such as sending mails or gathering content fromn webbrowser or opening applications etcetra'''
            speak(content)
            return
        elif 'gather' in command:
            speak("Gathering Please wait.....!!!")
            command = command.replace("gather", "")
            res = wikipedia.summary(command,sentences=1)
            print("According to wikipedia",res)
            speak("According to wikipedia ")
            speak(res)
        elif 'files' in command:
            print("These are files i can accesss \n1. C Drive\n2. D Drive\n3. E Drive\n4. Pictures\n5. Download\n6. Music\n7. Videos\n")
            speak("These are files i can accesss \n1. C Drive\n2. D Drive\n3. E Drive\n4. Pictures\n5. Download\n6. Music\n7. Videos\n")
            speak("Please give the numbers in the form of numbers below, because microphone cannot get the number. so, kindly enter the numbers")
            choice = int(input(""))
            file_path = set_path(choice)
            os.startfile(file_path)
        elif 'search' in command:
            query = " "
            for i in command.split(" "):
                if(i != "search"):
                    query += i+" " 
            webbrowser.open("https://www.google.com/search?q="+query)
            speak("This what i had found on web!!!")
        elif 'youtube' in command:
            speak("Do you want to open youtube or search any video")
            speak("If you want to open only youtube then say skip")
            speak("If you want search any video then say video and your input")
            command = takecommand().lower()
            query = " "
            if(command == "skip"):
                webbrowser.open("https://www.youtube.com")
            else:
                for i in command.split(" "):
                    if(i != "video"):
                        query += i+" "
                webbrowser.open("https://www.youtube.com/results?search_query="+query)
            speak("Opening Youtube")
        elif 'facebook' in command:
            webbrowser.open("https://www.facebook.com/")
            speak("Opening facebook")
        elif 'date' in command:
            res = datetime.datetime.now().date()
            print("today's date is : ",res)
            speak("today's date is ")
            speak(res)
        elif 'time' in command:
            res = datetime.datetime.now().strftime("%H:%M:%S")
            print("Now time is : ",res)
            speak("Now time is :")
            speak(res)
        elif 'email' in command:
            try:
                speak("Whom do you want to send this mail, Please Enter the mail id!! ")
                
                to = input("Enter the mail id here ->  ")
                speak("What should I say?") 
                content = takecommand()
                content = content + " --- This mail is System generated"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry!!. I am not able to send this email")
        elif 'network' in command:
            speak("The network will be shown what network you used before you shift from another operator ")
            speak("Enter ten digit mobile with country code and followed by mobile number")
            print("Enter the mobile with country code : ")
            number = input()
            network_finder(number)
        elif 'message' in command:
            speak("Enter ten digit mobile ")
            print("Enter the mobile : ")
            number = input()
            speak("What should i say?")
            content = takecommand()
            content = content + " --- This message is System generated"
            msg(number, content)
        elif 'weather' in command:
            speak("Your current location is vishakhapatnam")
            loc = "Vishakhapatnam"
            weather(loc)
        elif 'game' in command:
            speak("Pick any one of the game from two games")
            print("Pick a game\n1.Rock paper scissors\n2.Jumble Words : ")
            num = int(input())
            if(num == 1):
                ga.game()
            elif num==2:
                ga.game1()
            speak("Game over")
            print("Game over")
            speak("It's fun to play with you Thank you")

    except:
        speak("I didn't got")
        return

if __name__ == "__main__":

    welcome()
    greet = ["hi sir","hello sir"]
    
    while(1):
        speak("Please say your command")
        command = takecommand().lower()
        if "hi" in command or "hello" in command:
            num = random.randint(0,len(greet)-1)
            speak(greet[num])

        if 'exit' in command or 'quit' in command or 'sleep' in command:
            print("exiting, Bye Now!!")
            speak("exiting, Bye Now!!")
            exit()

        process_query(command)
import subprocess
import wolframalpha
import pyttsx3
import SpeechRecognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from ecapture import ecapture as ec
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use female voice

# Function to speak text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to greet the user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

    speak("I am your Assistant. How can I assist you today?")

# Function to take voice input from user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Unable to Recognize your voice.")
        return "None"
    return query.lower()

# Function to send email
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@example.com', 'your_password')  # Replace with your email and app password
        server.sendmail('your_email@example.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("I am not able to send this email.")

if __name__ == '__main__':
    wishMe()
    
    while True:
        query = takeCommand()

        # Logic for executing tasks based on the query

        # Wikipedia search
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Open websites
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        # Play music from a local directory
        elif 'play music' in query:
            music_dir = "C:\\Users\\GAURAV\\Music"  # Update this to your music directory
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        # Tell the current time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        # Send email
        elif 'email to' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "receiver_email@example.com"  # Replace with receiver's email
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("I am not able to send this email.")

        # Simple greetings and conversations
        elif 'how are you' in query:
            speak("I am fine, Thank you.")
            speak("How are you, Sir?")
        
        elif 'fine' in query or "good" in query:
            speak("It's good to know that you're fine.")

        elif 'who made you' in query or 'who created you' in query:
            speak("I have been created by Gaurav.")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        # WolframAlpha for calculations or complex questions
        elif 'calculate' in query:
            app_id = "your_wolframalpha_api_key"  # Replace with your WolframAlpha API key
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            speak(f"The answer is {answer}")

        # Weather information
        elif 'weather' in query:
            api_key = "your_openweather_api_key"  # Replace with your OpenWeather API key
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak("Which city?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            weather_data = response.json()

            if weather_data["cod"] != "404":
                main = weather_data["main"]
                temperature = main["temp"]
                pressure = main["pressure"]
                humidity = main["humidity"]
                weather_desc = weather_data["weather"][0]["description"]
                speak(f"The temperature is {temperature - 273.15:.2f} degrees Celsius.")
                speak(f"Atmospheric pressure is {pressure} hPa.")
                speak(f"Humidity is {humidity} percent.")
                speak(f"The weather description is {weather_desc}.")
            else:
                speak("City Not Found.")

        # Exit the assistant
        elif 'exit' in query:
            speak("Thank you for your time. Have a great day!")
            break

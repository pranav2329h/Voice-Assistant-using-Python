import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = aa.Recognizer()
machine = pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instraction():
    try:
        with aa.Microphone() as origin:
            print("listening...")
            speech = listener.listen(origin)
            instraction = listener.recognize_google(speech)  
            instraction = instraction.lower()
            if "lala" in instraction:
                instraction = instraction.replace('lala', "")
                print(instraction)            
            return instraction
    except:
        return None  

def play_lala():
    instraction = input_instraction()

    if instraction:  
        print(instraction)
        
        if "play" in instraction:
            song = instraction.replace("play", "")
            talk("playing " + song)
            pywhatkit.playonyt(song)
            
        elif 'time' in instraction:
            time = datetime.datetime.now().strftime('%I:%M %p')  
            talk('Current time: ' + time)
            
        elif 'date' in instraction:  
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            talk("Today's date: " + date)
            
        elif 'how are you' in instraction:
            talk('I am fine, how about you?')
            
        elif 'what is your name' in instraction:
            talk('I am Lala, what can I do for you?')
        
        elif 'who is' in instraction:
            human = instraction.replace('who is', "")
            info = wikipedia.summary(human, 1)
            print(info)
            talk(info)
            
        else:
            talk('Please repeat.')
    else:
        print("No instruction received, please try again.")  


while True:
    play_lala()


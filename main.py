import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import os
import requests
from openai import OpenAI

#pip install pocketsphinx

engine=pyttsx3.init()
newsapi="YOUR-API-KEY"

def speak(text):
    print(f"Eon says: {text}")
    engine = pyttsx3.init('sapi5')      # fresh engine each call
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiProcess(command):
    client = OpenAI(api_key="YOUR-API-KEY")
    completion=client.chat.completions.create(
        model="gpt-3.5-turbo-instruct",
        messages=[{"role": "system", "content": "You are a virtual assistant named eon skilled in general tasks like Alexa and Google Cloud"},{"role": "user", "content": command}]
)
    return completions.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        song = " ".join(c.lower().split(" ")[1:])  # join list into string
        try:
            link = musiclibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        except KeyError:
            speak(f"Sorry, I couldn’t find {song} in your music library.")
    elif "news" in c.lower():
        url = "URL here"

        # Fetch news
        response = requests.get(url)
        data = response.json()

        # Extract article titles and descriptions
        articles = data.get('results', [])

        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            description = article.get('description', 'No description')
            
            # Speak the title
            speak(f"Article {i}: {title}")

    else:
        #Let OpenAI handle the request
        output=aiProcess(c)
        speak(output)



if __name__=="__main__":
    speak("Initializing Eon")
    while True:
        #Listen for the wake word 'Eon'

        # obtain audio from the microphone
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=5,phrase_time_limit=3)
            word=r.recognize_google(audio)
            print("Heard:", word)
            if(word.lower()=="eon"):
                speak("Yes Sir")
                #Listen for command
                with sr.Microphone() as source:
                    print("Eon Active...")
                    audio = r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
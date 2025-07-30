from distutils.ccompiler import gen_preprocess_options
from pip import main
import pyttsx3      #text to speech module, reads strings
from datetime  import datetime  #date and time module
import speech_recognition as sr    #speech recognition module, takes voice input and converts it into a string
import wikipedia    #wikipedia module, gets information from wikipedia
import webbrowser   #browser module, opens links in browser tabs
import os           #used to perform various tasks on the operating system
import subprocess
import pyjokes
from playsound import playsound     #plays sound/music present on the computer
from time import sleep  
import requests
import json
import cv2
import psycopg2

# Connect to the database
conn = psycopg2.connect(
    dbname="virtualassistant",
    user="postgres",
    password="Rashuse@786",
    host="localhost",
    port="5432"
)

# Create a cursor
cur = conn.cursor()

engine= pyttsx3.init('sapi5')       #Microsoft speech api
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)       #Sets the voice of the Virtual assistant (MALE/FEMALE)
cap = cv2.VideoCapture(0)
    
path= 'C:\\Users\\mustu\\OneDrive\\Documents\\GitHub\\rcoe22-sem3-group7\\Acorn-Sound-Effect.mp3'  #path of the sound queue to be played

name=""

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def Wishme():
    speak("Initiating...")
    print("Initiating...")
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("What is your name?")
        speak("What is your name?")
        playsound(path)                 #plays a sound queue for the user to let them know when to speak
        print("\nListening...")
        r.pause_threshold = 1             #seconds before a phrase is considered complete
        audio=r.listen(source)
        global name                     #declaring a global variable that can be used throughout the program
        name=r.recognize_google(audio, language=('en-in'))
        print(f"The user said: {name}\n")

    hour=int(datetime.now().hour)          #gets the time from the system clock
    if hour>=0 and hour<12:
        print(f"Good Morning, {name}")
        speak(f"Good Morning, {name}")
    elif hour>=12 and hour<18:
        print(f"Good Afternoon, {name}")
        speak(f"Good Afternoon, {name}")
    elif hour>=19 and hour<24:
        print(f"Good Evening, {name}")
        speak(f"Good Evening, {name}")
    print(f"My name is Eve, How may I assist you?")
    speak(f"My name is Eve, How may I assist you?") 
    

def takecommand():                    #takes command from user through the microphone
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        playsound(path)               #plays a sound queue for the user to let them know when to speak
        r.pause_threshold=1           #seconds before a phrase is considered complete
        audio=r.listen(source)
    try:
        print("Recognising...")
        speak("Recognizing")
        query = r.recognize_google(audio, language=('en-in'))       #using speech recognition API from google
        print(f"The user said: {query}\n")

    except Exception as e:                      #exception handling, used to handle any errors that a program might throw
        print("Say that again please")
        speak("Say that again please") 
        return "None"
    return query   

def note(statement):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"   #code for taking notes
    with open(file_name, "w") as f:
        f.write(statement)    

def clear():
        os.system('cls')

def weather(city):
    API_key="25dd7cd96ab76fcfd31c67228e42f418"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    response = requests.get(url)    # Making a get request to the API
    res = response.json()       # Converting JSON response to a dictionary
    # print(res)                # Prints all the data fetched from the api
    if res["cod"] != "404":         # Checking if the city is found. If the value of "cod" is not 404, that means the city is found
        data = res["main"]
        temp = data["temp"]
        feel=data["feels_like"]
        pressure = data["pressure"]
        country=res["sys"]
        cname=country["country"]
        desc = res["weather"]
        weather_desc = desc[0]["description"]
        cel=int(temp)-273.15
        fcel=int(feel)-273.15
        print(f"Location: {city},{cname}")
        speak(f"Location:{city},{cname}")
        print(f"Temperature: {str(round(cel,2))} °C")
        speak(f"Temperature: {str(round(cel,2))} degree celcius")
        print(f"Feels like: {str(round(fcel,2))} °C")
        speak(f"Feels like:{str(round(fcel,2))} degree celcius")
        print(f"Pressure: {str(pressure)}")
        speak(f"Pressure:{str(pressure)} ")
        time=datetime.now().strftime("%H:%M %p")
        s = datetime.now().strftime("%A")
        print(f"Time: {s}, {time}")
        speak(f"Time: {s}, {time}")
        print(f"Weather Description: {str(weather_desc)}")
        speak(f"Weather Description: {str(weather_desc)}")
    else:
        speak("That is not a valid city")
        print("That is not a valid city")

if __name__ == "__main__":
    clear()
    Wishme()
    while True:
        query = takecommand().lower()       #converts the accepted command from user into lowercase
        #add the name of the user
        namee = name
        # Define the command and output variables
        command = query
        # Get the current timestamp
        timestamp = datetime.now()

        # Execute the insert statement to add a new row to the command_history table
        insert_query = "INSERT INTO command_history (name,command, timestamp) VALUES (%s,%s,%s)"
        cur.execute(insert_query, (name,command, timestamp))
        # Commit the changes
        conn.commit()

        if 'wikipedia' in query:
            speak("Searching on wikipedia...")
            print("Searching on Wikipedia...")
            query=query.replace("wikipedia","")     
            results=wikipedia.summary(query, sentences=2)  #gives results from wikipedia in a 3 sentence summary
            print("According to Wikipedia,")
            speak("According to Wikipedia,")
            print(results)
            speak(results)
        
        elif 'weather' in query:    #gives the weather of the mentioned city
            print("What is the name of your city?")
            speak("What is the name of your city?")
            city=takecommand()
            weather(city)

        elif 'open vs code' in query:
            print("opening VS code")
            speak("Opening VS Code")
            codepath = "C:\\Users\\0men\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)       #opens vs code
            exit()

        elif 'the time' in query:
            time=datetime.now().strftime("%H:%M %p")
            print(f"The time right now is {time}")        #tells the time in hour, minute format
            speak(f"The time right now is {time}")


        elif 'open youtube' in query:
            print("Opening YouTube...")
            speak("Opening Youtube")
            webbrowser.open("youtube.com")
            exit()      #opens youtube 

        elif 'on youtube' in query:
            query=query.replace("search","").replace("on youtube","")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            exit()    #searches on youtube

        elif 'open browser' in query:
            print("Opening browser...")
            speak("Opening browser")
            webbrowser.open("google.com")   
            exit()    #opens Google

        elif 'on browser' in query or "on google" in query:  #searches for the given command on google
            print("Searching...")
            speak("Searching...")
            query=query.replace("on browser","").replace("search","")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            exit()

        elif 'note this' in query:    
            print("What do you want me to note?")
            speak("What do you want me to note?")
            Statement=takecommand()  
            note(Statement)    # takes notes
            print("Noted.")  
            speak("Noted.")

        elif 'joke' in query:       #can tell you one liner jokes
            joke=pyjokes.get_joke()
            print(joke)
            speak(joke)  

        elif 'open netflix' in query:       #opens netflix through browser
            webbrowser.open_new_tab("https://www.netflix.com/in") 
            speak("Netflix open now")
            exit()

        elif 'open prime video' in query:           #opens Amazon prime video through browser
            webbrowser.open_new_tab("primevideo.com") 
            speak("Amazon Prime Video open now")
            exit()

        #elif 'search' in query or 'play' in query:
            #query = query.replace("search", "")
            #query = query.replace("play", "")         
            #webbrowser.open(query) 

        elif "clear history" in query:
            print("Clearing history...")
            speak("Clearing history")
            sleep(2)
            clear()
            print("...History cleared")   
            speak("History cleared")    
            Wishme()   

        elif 'exit' in query or 'stop' in query or 'end' in query:               #exits the program
            speak("Ending program...")
            print("Ending program...")        
            hour=int(datetime.now().hour)          #gets the time from the system clock
            if hour>=0 and hour<6:
                print(f"Goodbye {name}, Sleep well.")
                speak(f"Goodbye {name}, Sleep well.")
            elif hour>=6 and hour<18:
                print(f"Goodbye {name}, Have a nice day.")
                speak(f"Goodbye {name}, Have a nice day.")
            else:
                print(f"Goodbye {name}, Enjoy your night.")
                speak(f"Goodbye {name}, Enjoy your night.")  
            exit()

        try:
            # Check if the user said "switch on the camera"
            if "switch on the camera" in query:
                print("Camera is switching on...")
                # Turn on the camera
                while True:
                    ret, frame = cap.read()
                    cv2.imshow('camera', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                # Release the camera and close the window
                cap.release()
                cv2.destroyAllWindows()
                print("Camera is switched off.")
                break
            if "switch off the laptop" in query:
                print("Turning off the laptop in 10 seconds.")
                time.sleep(10)
                os.system("shutdown /s /t 1")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print("Sorry, something went wrong: {}".format(e))
        
        
#and close the cursor and connection
cur.close()
conn.close()

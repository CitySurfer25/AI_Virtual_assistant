
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os 
import time

import speech_recognition as sr
import pyttsx3
import pywhatkit 
import pytz
import subprocess



SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
MONTHS=['january','february','march','april','may','june','july','august','september','october','november','december']
DAYS=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
DAY_EXTENSIONS=['rd','th','st','nd']
def speak(text):
    engine= pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
    
def get_audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        said=""
        try:
            said=r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception" + str(e))
    return said.lower()
""""
text=get_audio()
if "hello" in text:
    speak("Welcome Bro This is Enzo Here!")
if 'what is your name' in text:
    speak("My name is Enzo")
if 'play' in text:
    query=text.replace("Play","")
    speak("Playing the requested Song")
   pywhatkit.playonyt(query)
"""



def authenticate_google():
  
  creds = None
 
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
 
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    return service
  except HttpError as error:
    
    
      print(f"An error occurred: {error}")

def get_events(day, services):
  

  date = datetime.datetime.combine(day, datetime.datetime.min.time())
  end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
  utc = pytz.UTC
  date = date.astimezone(utc)
  end_date = end_date.astimezone(utc)

  events_result = (
      services.events()
      .list(
          calendarId='primary',
          timeMin=date.isoformat(),
          timeMax=end_date.isoformat(),
          singleEvents=True,
          orderBy='startTime',
      )
      .execute()
  )
  events = events_result.get("items", [])

  if not events:
    print("No upcoming events found.")
    speak("No Upcoming events for you")
  else:
    speak(f"You have {len(events)} events on this day")
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
      start_time = str(start.split("T")[1].split("-")[0])
      if int(start_time.split(":")[0]) < 12:
        start_time = start_time + "am"
      else:
        start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
        start_time = start_time + "pm"
      # Corrected indentation:
      speak(event["summary"] + ' at ' + start_time)


      
      

    
    

  
def get_date(text):
   
   
   text=text.lower()
   today=datetime.date.today()

   if text.count==('today')>0:
      return today
   
   day=-1
   day_of_week=-1
   month=-1
   year=today.year
   
   
   for word in text.split():
      
      if word in MONTHS:
          month = MONTHS.index(word)+1
      
      elif word in DAYS:
          day_of_week = DAYS.index(word)
      
      elif word.isdigit():
          day=int(word)
      
      else:
          for ext in DAY_EXTENSIONS:
            found=word.find(ext)
            if found>0:
                
                try:
                  day=int(word[:found])
                except:
                  pass
   if month <today.month and month !=-1:
      year=year+1
   if day<today.day and month==-1 and day!=-1:
      month= month+1
   if month==-1 and day==-1  and day_of_week!=-1:
      current_day_of_week=today.weekday()
      dif= day_of_week-current_day_of_week
      if dif<0:
         dif+=7
         if text.count("next")>=1:
            dif+=7
      return today+datetime.timedelta(dif)
   if month== -1 or day==-1:
      return None
      
   return datetime.date(month=month,day=day,year=year)
    
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


               
      
   
 

SERVICE=authenticate_google()
print("START")

text=get_audio().lower()


##TEST CASE: CLEARED
if "hello" in text:
    speak("Welcome Bro This is Enzo Here!")
if 'what is your name' in text:
    speak("My name is Enzo")
if 'play' in text:
    query=text.replace("Play","")
    speak("Playing the requested Song")
    pywhatkit.playonyt(query)


CALENDAR_STRS=['What do I have','Am I busy',"Do I have Plans",'Is There any']
NOTE_STRS=["make a note",'write this down','remember this']

if any(phrase in text for phrase in CALENDAR_STRS):
    for phrase in CALENDAR_STRS:
        if phrase in text:
            date = get_date(text)
            if date:
                get_events(date, SERVICE)
            else:
                speak("Please try again")

    





else:
    for phrase in NOTE_STRS:
        if phrase in text:
            speak("what would you like me to write down?")
            note_text=get_audio()
            note(note_text)
            speak("I have made a note on that.")




'''



'''
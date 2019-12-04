#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import sys 
import speech_recognition as sr
import smtplib
import webbrowser 
import requests
from pyowm import OWM
import youtube_dl
import wikipedia 
#import vlc
import urllib
#import urllib2
import json
from bs4 import BeautifulSoup as soup
import random
from time import strftime
import subprocess
from  pygame import mixer
import random


# In[3]:


#the method which will interpret user voice response


def mycommand():
    r=sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Ready ...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("You said "+ command +'\n')
        
    except sr.UnknownValueError:
        print('.....')
        #loop back to continue to listen for commands if unrecognizable speech is received
        command = mycommand()
    return command 
        
        


# In[4]:


#a method that will convert text to speech.

def assistantTalks(audio):
    print(audio)
    spe  =gTTS(audio, lang='en-uk')
    spe.save("spe.mp3")
    playSound("spe.mp3")
    


# In[5]:



def playSound(file):
    #///////////////////////////////////////////////////////////
    #Jouer un(e) son/musique contenu(e) dans le fichier mp3 file 
    #///////////////////////////////////////////////////////////
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    


# In[7]:


def assistant(command):
    
    errors=[
        "I don\'t know what you mean!",
        "Excuse me?",
        "Can you repeat it please?",
           ]
    
    state=["I'm fine, I hope you're fine too!"
           ,"I'm doing good!",
           "I have never been better"]
    
    #///////////////////
    #Ouvrir une page web 
    #//////////////////
    if'hello' in command:
        assistantTalks("Hello Cilia, what can I do for you?")
        
        """ 
         day_time = int(strftime('%H'))
        if day_time < 12:
            assistantTalks('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            assistantTalks('Hello Sir. Good afternoon')
        else:
            assistantTalks('Hello Sir. Good evening')
        
        """
        
    if 'How are you' in command:
        assistantTalks(random.choice(state))
       
    #//////////////////
    #Decrire la meteo  
    #//////////////////
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
             city = reg_ex.group(1)
             owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
             obs = owm.weather_at_place(city)
             w = obs.get_weather()
             k = w.get_status()
             x = w.get_temperature(unit='celsius')
             assistantTalks('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
    #////////////////////
    #Mentionner le temps 
    #///////////////////
    elif 'time' in command:
         import datetime
         now = datetime.datetime.now()
         assistantTalks('Current time is %d hours %d minutes' % (now.hour, now.minute))
            
    #///////////////////
    #Salutations
    #//////////////////        
    elif  'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            assistantTalks('The website you have requested has been opened for you Sir.')
            
            
    elif 'email' or 'gmail' in command:
        assistantTalks("What is the subject? ")
        time.sleep(3)
        subject= mycommand()
        assistantTalks("What should i say? ")
        time.sleep(3)
        message= mycommand()
        
        content= 'Subject {}\n\n{}'.format(subject, message)
        #init gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        #identify to server
        mail.ehlo()

        #encrypt session
        mail.starttls()

        #login
        mail.login('your_gmail', 'your_gmail_password')

        #send message
        mail.sendmail('FROM', 'TO', content)

        #end mail connection
        mail.close()
        
            
   
        
    elif 'play' in comamnd:
        reg_e  = re.search('play ((.+)\s)+ ', command) 
        name = reg_ex.group(1)
        path = 'C://Users//ezi//Downloads//' + name +'.mp3'
        ## PRBOBLEM ESPACES 
        playSound(path)
    
    elif "where is" in comamnd:
        data = comamnd.split(" ")
        location = data[2]
        speak("Hold on Cilia, I will show you where " + location + " is.")
        os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")
            
            
    #///////////////////////
    #Mettre fin au programme 
    #//////////////////////
    
    elif 'shutdown' in command:
        assistantTalks('Bye bye Cilia. Have a nice day')
        sys.exit()
        
    #///////////////////
    #Ordre ambigu  
    #//////////////////
    else:
        error= random.choice(errors)
        assistantTalks(error)
        
mycommand()
#loop to continue executing multiple commands
while True:
    assistant( mycommand())


# In[ ]:





#IDS Gruppe 5 - Jokes Application

#https://api.imgflip.com/get_memes                  - The list of memes API                
#https://official-joke-api.appspot.com/random_joke  - The random joke generator API

import requests
import json
import socket 
import npyscreen
import random
from PIL import Image 

UDP_IP = "127.0.0.1"                
UDP_PORT = 5010                     # The UDP Port where the message will be sent to 
MESSAGE = b"Do you listen to jokes" # This sends a message to the UDP server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))                       

class App(npyscreen.NPSAppManaged):                                 
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)          
        self.addForm('MAIN', FirstForm, name="Joke Generator")      

class FirstForm(npyscreen.ActionForm, npyscreen.ThemeManager):      
    def create(self):
        self.add(npyscreen.TitleText, w_id='txt', name= "Welcome to my joke generator application interface", begin_entry_at=53)
        self.nextrely +=1
        self.add(npyscreen.TitleText, w_id="textfield", name="Enter your name:", begin_entry_at=19)
        self.add(npyscreen.ButtonPress, name="OK", when_pressed_function=self.btn_press)
        
    def btn_press(self):
        message = f'Hello, President {self.get_widget("textfield").value}' 
        mad = f'Here is a joke {self.get_widget("textfield").value}' 

        npyscreen.notify_confirm(message, title="Hello, President", wrap=True, wide=True, editw=1)
        npyscreen.notify_confirm(mad, title="The type of joke is,", wrap=False, wide=False, editw=1)

        api_address = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url=api_address)
        response = response.json()

        jokeType = response['type']
        setup = response['setup']
        punchline = response['punchline']   

        message = f'The type of joke is: {jokeType}'
        moms = f'The setup joke: {setup}'
        mans = f'The punchline: {punchline}'

        npyscreen.notify_confirm(message, title="Hi", wrap=False, wide=True, editw=1)
        npyscreen.notify_confirm(moms, title="Hi", wrap=False, wide=True, editw=1)
        npyscreen.notify_confirm(mans, title="Hi", wrap=False, wide=True, editw=1)
        npyscreen.notify_wait("Can you recognize this picture")

        sock.sendto(bytes(str(message), encoding='utf8'), (UDP_IP, 5010))   #These sockets sends the jokes to the UDP packet sender
        sock.sendto(bytes(str(moms), encoding='utf8'), (UDP_IP, 5010))
        sock.sendto(bytes(str(mans), encoding='utf8'), (UDP_IP, 5010))

        urli = "https://api.imgflip.com/get_memes"
        res = requests.get(url=urli)
        res = res.json()
        memi = res['data']['memes'][random.randint(0,100)]['url']           #Generates a random meme picture between 0-99
        im = Image.open(requests.get(memi, stream=True).raw)
        im.show()                                                           #Shows the meme picture
        
        sock.sendto(bytes(str(memi), encoding='utf8'), (UDP_IP, 5010))      #This sends the link of the random meme picture to the packet sender

        with open('joker.txt','w') as file_out:                             #This stores the link of the meme on a txt file
            json.dump(memi, file_out)

    def on_ok(self):
        npyscreen.notify_wait(" OK button pressed!\n You are exiting the application", "OK Button!")
        self.parentApp.switchForm(None)

    def on_cancel(self):
        npyscreen.notify_yes_no("Are you done", editw=1)
        npyscreen.notify_wait(" Cancel button pressed!\n Bye have a good time.", "Cancel Button!")
        self.parentApp.switchForm(None)

app = App()
app.run()
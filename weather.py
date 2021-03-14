
#from npyscreen.wgtitlefield import TitleText  #måske bliver den brugt
#done with UDP 
#done with API 

#use threading 
#use json
#chatbot 
#UDP Package?
#ASCII Art?

import requests
import json
import socket
import npyscreen
import threading


UDP_IP = "127.0.0.1"
UDP_PORT = 5010
MESSAGE = b"Do you listen to jokes" # this sends a message to the UDP server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) # this sends text
           

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm('MAIN', FirstForm, name="Account Login")
        self.addForm('SECOND', SecondForm, name="Weather Report")

class FirstForm(npyscreen.ActionForm, npyscreen.SplitForm, npyscreen.FormWithMenus, npyscreen.ThemeManager):
    def create(self):
        self.add(npyscreen.TitleText, w_id='txt', name= "Welcome to my weather application interface", begin_entry_at=46)
        self.nextrely +=1
        self.add(npyscreen.TitleText, w_id="textfield", name="Enter your name:", begin_entry_at=19)
        self.add(npyscreen.TitleText, w_id="textfield", name="Enter your pasword:", begin_entry_at=22)
        self.add(npyscreen.ButtonPress, name="OK", when_pressed_function=self.btn_press)
        #self.add(npyscreen.ButtonPress, name="Cancel", when_pressed_function=self.on_cancel)
        #self.show_atx = 20 # changes the placement of the screen 
        #self.show_aty = 5 # changes the placement of the screen 

        self.menu = self.new_menu(name= "Main Menu", shortcut='m')
        self.menu.addItem("Item 1", self.press_1, "1")
        self.menu.addItem("Item 2", self.press_2, "2")
        self.menu.addItem("Exit Form", self.exit_form, "^X")

        self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        self.submenu.addItem("Change color")
        self.submenu.addItem("Option")
        self.submenu.addItem("Quit")

    def press_1(self):
        npyscreen.notify_confirm("You pressed item 1!", "Item 1", editw=1)

    def press_2(self):
        npyscreen.notify_confirm("You pressed item 2!", "Item 2", editw=1)

    def exit_form(self):
        self.parentApp.switchForm(None)
        
    def btn_press(self):
        message = f'Hello, President {self.get_widget("textfield").value}' 
        npyscreen.notify_confirm(message, title="Hello, President", wrap=True, wide=True, editw=1)

    def on_ok(self):
        npyscreen.notify_wait(" OK button pressed!\n Next page is coming", "OK Button!")
        self.parentApp.switchForm('SECOND')

    def on_cancel(self):
        npyscreen.notify_yes_no("Are you done", editw=1)
        npyscreen.notify_wait(" Cancel button pressed!\n Bye have a good time.", "Cancel Button!")
        self.parentApp.switchForm(None)

class SecondForm(npyscreen.ActionForm, npyscreen.ThemeManager):
    def create(self):
        self.add(npyscreen.TitleText, w_id="textfield", name="Enter city:")
        self.add(npyscreen.ButtonPress, name="Get weather report", when_pressed_function=self.btn_press)

    def btn_press(self):
        form_input = self.get_widget("textfield").value
        api_address = "http://api.openweathermap.org/data/2.5/weather?appid=888b39b5cf60b51865bc7d14c35150a5&q=" + form_input
        response = requests.get(url=api_address)

        #if response.text == '[]':
         #   npyscreen.notify_confirm("Search returns null", title="Hi", wrap=True, wide=True, editw=1)
         #   return

        response = response.json()

        weather = response['weather'][0]['main'] # weather information type
        weatherDescription = response['weather'][0]['description'] # description of weather
        weatherTemperature = response['main']['temp'] # information about temperature in kelvin. husk minus med -273.15
        countryShortName = response['sys']['country'] # shortened name of a country

        message = f'The weather: {weather}'
        meme = f'The temperature is {round(weatherTemperature-273.15)}'
        moms = f'The country name: {countryShortName}'
        mans = f'Weather description: {weatherDescription}'
        npyscreen.notify_confirm(message, title="Hi", wrap=True, wide=True, editw=1)
        npyscreen.notify_confirm(mans, title="Hi", wrap=True, wide=True, editw=1)
        npyscreen.notify_confirm(meme, title="Hi", wrap=True, wide=True, editw=1)
        npyscreen.notify_confirm(moms, title="Hi", wrap=True, wide=True, editw=1)

        UDP_IP = "127.0.0.1"
        UDP_PORT = 5010
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(bytes(str(message), encoding='utf8'), (UDP_IP, 5010))
        sock.sendto(bytes(str(meme), encoding='utf8'), (UDP_IP, 5010))
        sock.sendto(bytes(str(moms), encoding='utf8'), (UDP_IP, 5010))
        sock.sendto(bytes(str(mans), encoding='utf8'), (UDP_IP, 5010))

        #with open('bowser.json', 'w') as json_file:
         #   json.dump('jsonVariable', json_file)

    def on_ok(self):
        self.parentApp.switchForm(None)

    def on_cancel(self):
        npyscreen.notify_yes_no("Do you want to stop the weather report API", editw=1)
        self.parentApp.switchForm(None)

app = App()
app.run()
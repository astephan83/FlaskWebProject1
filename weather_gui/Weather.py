'''
Group B
Jamie Wimsatt, Zack Powell, Amanda Stephan
Weather Application:
The application’s goal is to retrieve data about the weather 
using OpenWeatherMap API and displaying a week long forecast 
in an application using a GUI. The application will also allow 
users to save settings, such as cities and default temperature. 
Also have an option to print out the forecast.

77dbc172aee4836d569ffcc9c4715602

'''

import sqlite3
import pyowm
import sys
#from PySide.QtCore import *
#from PySide.QtGui import *
import datetime
from time import localtime, time
from math import *
from builtins import super

#app = QApplication(sys.argv)
#win = QWidget()
owm = pyowm.OWM('77dbc172aee4836d569ffcc9c4715602')
FORCAST_DAYS = 5

def findDataType(data):
    return str(data), str(type(data)), str(super(data.__class__, data))

# Will it be sunny tomorrow at this time in Milan (Italy) ?
forecast = owm.daily_forecast("Milan,it")
tomorrow = pyowm.timeutils.tomorrow()
if forecast.will_be_sunny_at(tomorrow): # Always True in Italy, right? ;-)
  print("yep") 
else:
  print("nope")

# Search for current weather in 'City, state'
def forcast(city, state=None):
    if state == None:
        rqsted_city = city
    else:
        rqsted_city = city + ', ' + state

    forcast = owm.daily_forecast(rqsted_city, limit=FORCAST_DAYS)
    cast = forcast.get_forecast()
    lst = cast.get_weathers()
    print(city)
    for weather in cast:
        print(weather.get_reference_time('iso'), weather.get_status())
    print()

# get five dates starting from today
def get_dates():
    number_of_days = []
    for i in range(FORCAST_DAYS):
        number_of_days.append((localtime(time() + 24*3600 * i)[0], localtime(time() + 24*3600*i)[1], localtime(time() + 24*3600*i)[2]))
    #print(number_of_days)

    # return a list of tuples(year, month, day) for FORCAST_DAYS
    return number_of_days

get_dates()
    
observation = owm.weather_at_place('Tampa, FL') # AssurtionError if not string
w = observation.get_weather()
#print(w)                      # <Weather - reference time=2013-12-18 09:20, status=Clouds>

print(findDataType(w.get_temperature()))

'''
FUNCTIONS FOR GUI
'''
class Weather:
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    # search button (takes info from user to search for city)
    def search(self, city_state=None, zip=None):
        if zip != None:
            self._observation = owm.weather_at_place(zip)
        if city_state != None:
            self._observation = owm.weather_at_place(city_state)
        else:
            return
    # dispaly funciton
    def display(self):
        pass
    
# history tab click (max 10)

# saved cities tab (from database)

# save button (saves current search)

# setting icon (bings up new window with settings)

# city and state text box (input from user)

# zip text box (input from user)


''' ALARM POPUP TEST FOR QT 
app = QApplication(sys.argv)

try:
    # default message
    due = QTime.currentTime()
    message = "Alert"
    
    if len(sys.argv) < 2:
        raise ValueError
    
    hours, minutes = sys.argv[1].split(':')
    due = QTime(int(hours), int(minutes))
    
    if not due.isValid():
        raise ValueError
    
    # if user inputs a mesage after time, join into one string
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
    # if the user did not specify, Alert is default
    
except ValueError:
     message = "Ussage: pop.py HH:MM {optional message}" # 24 hout clock


while QTime.currentTime() < due:
    time.sleep(10)

label = QLabel('<font color=red size=72)<b>' + message + '</b></fort>')
label.setWindowFlags(Qt.SplashScreen)
label.show()

QTimer.singleShot(20000, app.quit) #20 seconds
app.exec_()
'''

''' Test QT CALCULATOR
class Form(QDialog):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.linedit = QLineEdit("Type an Expression and press Enter")
        self.linedit.selectAll()

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.linedit)
        self.setLayout(layout)

        self.linedit.setFocus()

        # connecting signal in of line edit to update the ui
        self.connect(self.linedit, SIGNAL("returnPressed()"), self.updateUi)
        self.setWindowTitle("Calculate")

    def updateUi(self):
        try:
            text = self.linedit.text()
            self.browser.append("%s = <b>%s<b>" % (text, eval(text)))
        except:
            self.browser.append("<font color=red>%s is invalid</font>" % text)

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
'''
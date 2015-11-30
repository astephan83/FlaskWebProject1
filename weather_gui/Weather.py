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
import sys
from time import localtime, time
import datetime
from math import *
sys.path.append('C:\Python34\Lib\site-packages')
import pyowm
import database_queries

owm = pyowm.OWM('77dbc172aee4836d569ffcc9c4715602')
FORCAST_DAYS = 5
DAYOFWEEK = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
TEMP_UNIT = {'K':'kelvin', 'C':'celsius', 'F':'fahrenheit'}

# Search for current weather in 'City, state'
def forcast(city, state=None, tmp_unit='F'):
    if state == None:
        rqsted_city = city
    else:
        rqsted_city = city + ', ' + state

    forcast = owm.daily_forecast(rqsted_city, limit=FORCAST_DAYS)
    cast = forcast.get_forecast()
    lst = cast.get_weathers()
    #print(city)
    dates = get_dates()
    temps = []
    
    #for date in dates:
    #    date_temps = one_day_forcast(forcast, city, state, date, tmp_unit)
    #    temps.append(date_temps)
    
    return_list = []
    #print(cast,dates)
    for weather, date in zip(cast,dates):
        return_list.append((weather.get_detailed_status(), date, database_queries.get_icon(None, weather.get_detailed_status())))
    #print(return_list)
    return return_list # returns list of ['weather', (year, month, day, day_of_week), icon, (min_temp, max_temp)]

# get five dates starting from today
#
#    returns list of tuples (year, month, day, day_of_week)
def get_dates():
    dates = []
    for i in range(FORCAST_DAYS + 1):
        dates.append((localtime(time() + 24*3600 * i)[0], localtime(time() + 24*3600*i)[1], localtime(time() + 24*3600*i)[2], DAYOFWEEK[localtime(time() + 24*3600*i)[6]]))

    # return a list of tuples(year, month, day) for FORCAST_DAYS
    return dates

# get the forcast for one day 
#    date should be a list of year, month, day
#    returns a tuple of ints (min_temp, max_temp)
def one_day_forcast(forcast, city, state=None, date=None, tmp_unit='F'):
    next_date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), 12, 0)
    weather = forcast.get_weather_at(next_date)
    if state != None:
        w = weather.weather_at_place(city + ',' + state)
    else:
        w = weather.weather_at_place(city)

    temp = w.get_temperature(TEMP_UNIT[tmp_unit])
    return temp['temp_min'], temp['temp_max'] # weather object

# get the current tempurature
#  
#    returns a tuple of ints
def temp(city, state=None, tmp_units='F'):
    if state != None:
        observation = owm.weather_at_place(city + ',' + state)
    else:
        observation = owm.weather_at_place(city)
    weather = observation.get_weather()
    temps = weather.get_temperature(TEMP_UNIT[tmp_units])

    return temps[2], temps[3]
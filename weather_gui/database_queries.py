'''database_queries.py
This file is for sql queries made to the SQLite database'''

import sqlite3 as sqlt
import sys

connection = None

'''
    Gets url for icon 
    
    Parameters: icon_number(int) - id code specified from openweathermap library 
                description(string) - description of id based on openweathermap
                is_night(bool) - checks if night or day - only True for clear sky, few clouds and broken clouds
    Returns:
        row - returns url or urls based on exact description
'''
def get_icon(id_number, description=None, is_night='False'):
    try:
        connection = sqlt.connect('weather.db')
        
        with connection:
            conn = connection.cursor()

            if id_number != None:
                if is_night == True:
                    id_number += 10

                conn.execute("SELECT icon FROM weather_icons WHERE pid=? AND isNight=?", (id_number, is_night))

            elif description != None:
                statement = "SELECT w.icon FROM weather_icons w WHERE (w.description='"+description+"' OR w.description LIKE '%"+description+"%') AND w.isNight = '"+is_night+"'"
                conn.execute(statement)

            row = conn.fetchall()

            return row

    except sqlt.Error as e:
        if connection:
            connection.rollback()
        print("Error {0}: ".format(e.args[0]))
        
    finally:
       if connection:
           connection.close() 



'''
    Gets the description of icon

    Parameters:
        id_number(int) - id code specified from openweathermap library 
        is_night(bool) - checks if is night - only True for clear sky, few clouds and broken clouds

    Returns:
        desc - description of icon
'''
def get_description(id_number, is_night=False):
    try:
        connection = sqlt.connect('weather.db')
        
        if is_night == True:
            id_number += 10

        with connection:
            conn = connection.cursor()
            conn.execute("SELECT description FROM weather_icons WHERE pid=? ", (id_number,))
            desc = conn.fetchone()

            return desc

    except sqlt.Error as e:
        if connection:
            connection.rollback()
        print("Error {0}: ".format(e.args[0]))
        
    finally:
       if connection:
           connection.close() 



'''
    Saves city settings to database

    Parameters:
        city_name(string) - location name and state 
        temp(char) - character to determine if C(Celsius), F(Fahrenheit), or K(Kelvin)

    Returns:
        status - if saved successfully or failed
'''
def save_city(city_name, temp):
    try:
        connection = sqlt.connect('weather.db')

        with connection:
            conn = connection.cursor()
            conn.execute("INSERT INTO settings (city_name, temperature) VALUES ('"+ city_name+"','"+ temp+"')")
            connection.commit()

    except sqlt.Error as e:
        if connection:
            connection.rollback()
        print("Error {0}: ".format(e.args[0]))
        
    finally:
       if connection:
           connection.close() 


'''
    Gets list of cities saved

    Parameter:
        None

    Returns:
        rows - list of cities and temperatures returned
'''
def get_saved_cities():
    try:
        connection = sqlt.connect('weather.db')

        with connection:
            conn = connection.cursor()
            conn.execute("SELECT * FROM settings")

            rows = conn.fetchall()

    except sqlt.Error as e:
        if connection:
            connection.rollback()
        print("Error {0}: ".format(e.args[0]))
        
    finally:
       if connection:
           connection.close() 
       return rows


'''
    Updates settings in database

    Parameters:
        id(int): id number used in table to find specific setting
        
    Returns:  
        status - if saved successfully or failed
'''
def update_settings(city_name, temp, id):
    try:
        connection = sqlt.connect('weather.db')

        with connection:
            conn = connection.cursor()
            conn.execute("UPDATE settings SET city_name=?, temperature=? WHERE sid=?;", (city_name, temp, id))
            connection.commit()

    except sqlt.Error as e:
        if connection:
            connection.rollback()
        print("Error {0}: ".format(e.args[0]))
        
    finally:
       if connection:
           connection.close() 


'''
    Deletes a setting from database

    Parameters:
        id(int): id number used in table to find specific setting
        
    Returns:  
        status - if saved successfully or failed
'''
def delete_setting(id):
    try:
        connection = sqlt.connect('weather.db')

        with connection:
            conn = connection.cursor()
            conn.execute("DELETE FROM settings WHERE sid=?;", (id,))
            connection.commit()

    except sqlt.Error as e:
        if connection:
            connection.rollback()
        print("Error {0}: ".format(e.args[0]))
        
    finally:
       if connection:
           connection.close() 
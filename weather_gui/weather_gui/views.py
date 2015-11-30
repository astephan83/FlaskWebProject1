"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify, redirect, url_for
from weather_gui import app
import database_queries as dq
import Weather 

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/get_login')
def get_login():
    message = ''
    user = request.args.get('user', "", type=str)
    password = request.args.get('password', "", type=str)
    data = dq.get_password(user)
    #print(data)
    if(data[0][0] == password):
        message = data
        #return redirect(url_for('home', username=str(data[0][1])))
    else:
        message = "error"
    return jsonify(message=message)

@app.route('/login_new')
def login_new():
    return render_template('new_user.html')

@app.route('/save_login')
def save_login():
    message = ''
    user = request.args.get('user', "", type=str)
    password = request.args.get('password', "", type=str)
    print(user, password)
    message = dq.save_login(user, password)
    return jsonify(message=message)

@app.route('/home/<username>')
def home(username):
    print("here")
    history = ""
    saved_results = ""
    
    if(username != 'guest'):
        saved_results = dq.get_saved_cities(int(username))

    """Renders the home page."""
    return render_template(
        'main.html',
        date = datetime.now().date(),
        saved_results = saved_results,
        history = history, 
        username = username
    )

@app.route('/get_city_forecast')
def get_city_forecast():
    city = request.args.get('city', "", type=str)
    temp = request.args.get('temp', "", type=str)
    forecast_by_name = city.split(",")

    if(len(forecast_by_name) > 1):
        forecast = Weather.forcast(forecast_by_name[0],forecast_by_name[1], temp)
    else:
        forecast = Weather.forcast(forecast_by_name[0],None, temp) 
    return jsonify(city_name=city, five_day=forecast)

@app.route('/settings')
def settings():
    return "Put settings page here"
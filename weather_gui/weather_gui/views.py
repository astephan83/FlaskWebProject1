"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from weather_gui import app
import database_queries as dq
import Weather 

@app.route('/')
@app.route('/home')
def home():
    history = []
    saved_results = dq.get_saved_cities()

    """Renders the home page."""
    return render_template(
        'main.html',
        date = datetime.now().date(),
        saved_results = saved_results,
        history = history
    )

@app.route('/get_city')
def get_city():
    city = request.args.get('city', "", type=str)
    forecast_by_name = city.split(",")
    if(len(forecast_by_name) > 1):
        forecast = Weather.forcast(forecast_by_name[0],forecast_by_name[1])
    else:
        forecast = Weather.forcast(forecast_by_name[0]) 
    return jsonify(city_name=city, five_day=forecast)

@app.route('/settings')
def settings():
    return "Put settings page here"
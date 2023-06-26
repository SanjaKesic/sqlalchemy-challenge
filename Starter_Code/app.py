# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import func


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

# Create an instance of Flask
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


# Create an instance of Flask


# Define the home route
@app.route("/")
def home():
    """List all available routes"""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data"""
    # Calculate the date one year from today
    one_year_ago = dt.date.today() - dt.timedelta(days=365)
    
    # Query the database for precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Create a dictionary with date as the key and precipitation as the value
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query the database for the list of stations
    results = session.query(Measurement.station).distinct().all()
    
    # Extract the station names from the results
    station_names = [station[0] for station in results]
    
    return jsonify(station_names)

# Define the temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the last 12 months of temperature observation data"""
    # Calculate the date one year from today
    one_year_ago = dt.date.today() - dt.timedelta(days=365)
    
    # Query the database for temperature observations for the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()
    
    # Create a list of dictionaries with date and temperature observations
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]
    
    return jsonify(tobs_data)

# Define the start date route
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return the minimum, average, and maximum temperatures for a given start date"""
    # Query the database for temperature data greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    # Create a dictionary with temperature statistics
    temperature_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    
    return jsonify(temperature_stats)

# Define the start and end date route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return the minimum, average, and maximum temperatures for a given start and end date"""
    # Query the




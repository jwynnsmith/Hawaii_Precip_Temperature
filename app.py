import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///hawaii.sqlite")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hawaii.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save reference to the table
#Passenger = Base.classes.passenger
Measurement = Base.classes.measurement
Station = Base.classes.station

# We can view all of the classes that automap found
Base.classes.keys()

# Create our session (link) from Python to the DB
session = Session(db.engine)




#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"api/v1.0/<start><br/>"
        f"api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def temps_dict():
    """Return a list of all passenger names"""
    # Query all passengers
    #results = session.query(Passenger.name).all()

    results = db.session.query(Measurement.date, Measurement.tobs).all()
    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))

# Create a dictionary from the row data and append to a list of all_temperatures
    temps_dict = {}
    for date, tobs in results:
        temps_dict[date] = tobs

    return jsonify(temps_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations
    results = db.session.query(Station.station).all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all temperatures
    results = db.session.query(Measurement.tobs).all()

    temps = list(np.ravel(results))

    return jsonify(temps)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dates(start=None, end=None):
     # Query temperatures with just start date"
    if not end:
        results = db.session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        temperatures = list(np.ravel(results))

        return jsonify(temperatures)
    # Query temperatures with between a start and end date
    results = db.session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temperatures = list(np.ravel(results))

    return jsonify(temperatures)


if __name__ == '__main__':
    app.run(debug=True)

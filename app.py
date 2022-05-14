# dependencies and set up
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///data/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for date and pcrp data
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to prcp_list
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def allstation():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for date and pcrp data
    results_2 = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results_2))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for date and tobs data
    results_3 = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date < '2017-08-23').filter(measurement.date > '2016-08-23').\
    filter(measurement.station == 'USC00519281').order_by(measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to USC00519281_list
    USC00519281_list = []
    for date, tobs in results_3:
        USC00519281_dict = {}
        USC00519281_dict["date"] = date
        USC00519281_dict["tobs"] = tobs
        USC00519281_list.append(USC00519281_dict)

    return jsonify(USC00519281_list)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

# Define function, set default value for end in case user does not input an end date
def startend(start= None, end= '2017-08-23'):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for date and tobs data based on input
    results_4 = session.query(measurement.date, measurement.tobs).filter((func.strftime(measurement.date) >= start),\
    (func.strftime(measurement.date) <= end)).order_by(measurement.date).all()

    session.close()

    # list for tobs data based on input
    tobs_input = []
    # list for aggregate values that we will calculate later
    tobs_agg = []

    #loop through data based on input date(s)
    for date, tobs in results_4:
        tobs_input.append(tobs)

    temp_min = min(tobs_input)
    temp_max = sum(tobs_input)/len(tobs_input)
    temp_avg = max(tobs_input) 

    tobs_agg = [temp_min, temp_max, temp_avg]

    return jsonify(tobs_agg)


if __name__ == "__main__":
    app.run(debug=True)
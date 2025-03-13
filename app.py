from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
        
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
        
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)
        
        Total_stops = int(request.form["stops"])
        
        airline = request.form['airline']
        airlines = ['Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 'SpiceJet', 'Vistara', 'GoAir',
                    'Multiple carriers Premium economy', 'Jet Airways Business', 'Vistara Premium economy', 'Trujet']
        airline_values = [1 if airline == name else 0 for name in airlines]
        
        Source = request.form["Source"]
        sources = ['Delhi', 'Kolkata', 'Mumbai', 'Chennai']
        source_values = [1 if Source == name else 0 for name in sources]
        
        Destination = request.form["Destination"]
        destinations = ['Cochin', 'Delhi', 'New_Delhi', 'Hyderabad', 'Kolkata']
        destination_values = [1 if Destination == name else 0 for name in destinations]
        
        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            *airline_values,
            *source_values,
            *destination_values
        ]])

        output = round(prediction[0], 2)
        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

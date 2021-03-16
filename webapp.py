from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html', response = get_state_options())

@app.route("/response")
def render_response():
    state_selected = request.args['states']
    return render_template('response.html', response = get_state_options(), fact = average_median_houseold_income(state_selected))

def get_state_options():
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    listOfStates = []
    options = ""
    for county in counties:
        if county["State"] not in listOfStates:
            listOfStates.append(county["State"])
    for state in listOfStates:
        s = state[0:2]
        options += Markup("<option value=\"" + s + "\">" + s + "</option>")
    return options

def average_median_houseold_income(the_state):
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    counties_in_state = []
    for county in counties:
        if county["State"] == the_state:
            counties_in_state.append(county["Income"]["Median Houseold Income"])
    sum = 0.0
    for x in counties_in_state:
        sum += x
    average = int(sum//len(counties_in_state))
    average = str(average)
    returned_string = "The average median houseold income of " + the_state + "is $" + average
    return returned_string

if __name__=="__main__":
    app.run(debug=True)

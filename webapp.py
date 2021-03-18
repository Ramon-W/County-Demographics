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
    return render_template('response.html', response = get_state_options(), responseTwo = get_county_options(state_selected), statefact = average_median_houseold_income(state_selected))

@app.route("/responseTwo")
def render_responseTwo():
    county_selected = request.args['county']
    county_selected.replace("+", " ") 
    return render_template('response.html', reponse = get_state_options(), responseTwo = get_county_options(state_selected), countyfact = get_high_school_education(county_selected))

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

def get_county_options(state_select):
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    listOfCounties = []
    options = ""
    for county in counties:
        if county["State"] == state_select:
            listOfCounties.append(county["County"])
    for county in listOfCounties:
        options += Markup("<option value=\"" + county + "\">" + county + "</option>")
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
    returned_string = "The average median houseold income of " + the_state + " is $" + average
    return returned_string

def get_high_school_education(county_select):
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    school_percent = "In " + county_select + ", " + county_select["Education"]["High School Education"] + "% have a high school education."
    return school_percent

if __name__=="__main__":
    app.run(debug=True)

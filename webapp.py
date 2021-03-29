from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html', response = get_state_options(), responseTwo = get_county_options())

@app.route("/response")
def render_response():
    with open('county_demographics.json') as demographics_data:
        count = json.load(demographics_data)
    state_selected = request.args['states']
    county_selected = request.args['county']
    county_selected.replace("+", " ") 
    data_selected = request.args['data']
    return render_template('home.html', response = get_state_options(count), responseTwo = get_county_options(count), statefact = average_median_houseold_income(state_selected, count), countyfact = get_high_school_education(county_selected, count), data = get_fact(data_selected, state_selected, count), unrelated = "Unrelated Facts:")

def get_state_options(counties):
    listOfStates = []
    options = ""
    for county in counties:
        if county["State"] not in listOfStates:
            listOfStates.append(county["State"])
    for state in listOfStates:
        s = state[0:2]
        options += Markup("<option value=\"" + s + "\">" + s + "</option>")
    return options

def get_county_options(counties):
    options = ""
    for county in counties:
        options += Markup("<option value=\"" + county["County"] + "\">" + county["County"] + "</option>")
    return options

def get_fact(the_data, selected_state, counties):
    counties_in_state = []
    returned_string = ""
    for county in counties:
        if county["State"] == selected_state:
            if the_data == 'Income':
                counties_in_state.append(county["Income"]["Per Capita Income"])
    sum = 0.0
    for x in counties_in_state:
        sum += x
    average = int(sum//len(counties_in_state))
    average = str(average)
    if the_data == 'Income':
        returned_string = "The average per capita income of " + selected_state + " is $" + average + ", and "
    
    county_name = counties[0]["County"]
    county_data = 0
    if the_data == 'Income':
        county_data = counties[0]["Income"]["Per Capita Income"]
        for county in counties:
            if county["State"] == selected_state and county["Income"]["Per Capita Income"] > county_data:
                county_data = county["Income"]["Per Capita Income"]
                county_name = county["County"]
        return returned_string + county_name + " has the highest per capita income of " + selected_state + ": $" + str(county_data) 
    else:
        return ""

def average_median_houseold_income(the_state, counties):
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

def get_high_school_education(county_select, counties):
    school_percent = ""
    for county in counties:
        if county["County"] == county_select:
            percent = str(county["Education"]["High School or Higher"])
            school_percent = "In " + county_select + ", " + percent + "% have at least a high school education."
    return school_percent

if __name__=="__main__":
    app.run(debug=True)

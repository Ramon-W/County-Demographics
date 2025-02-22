from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html', response = get_state_options(), responseTwo = get_county_options())

@app.route("/response")
def render_response():
    state_selected = request.args['states']
    county_selected = request.args['county']
    county_selected.replace("+", " ") 
    data_selected = request.args['data']
    return render_template('home.html', response = get_state_options(), responseTwo = get_county_options(), statefact = average_median_houseold_income(state_selected), countyfact = get_high_school_education(county_selected), data = get_fact(data_selected, state_selected), unrelated = "Unrelated Facts:")

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

def get_county_options():
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    options = ""
    for county in counties:
        options += Markup("<option value=\"" + county["County"] + "\">" + county["County"] + "</option>")
    return options

def get_fact(the_data, selected_state):
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    counties_in_state = []
    diversity = 0.0
    returned_string = ""
    for county in counties:
        if county["State"] == selected_state:
            if the_data == 'Income':
                counties_in_state.append(county["Income"]["Per Capita Income"])
            elif the_data == 'Education':
                counties_in_state.append(county["Education"]["Bachelor's Degree or Higher"])
            elif the_data == 'Homeownership':
                counties_in_state.append(county["Housing"]["Homeownership Rate"])
            elif the_data == 'Employment':
                counties_in_state.append(county["Employment"]["Private Non-farm Employment Percent Change"])
            elif the_data == 'Diversity':
                diversity = 100.0 - county["Ethnicities"]["White Alone, not Hispanic or Latino"]
                counties_in_state.append(diversity)
    sum = 0.0
    for x in counties_in_state:
        sum += x
    average = int(sum//len(counties_in_state))
    average = str(average)
    if the_data == 'Income':
        returned_string = "The average per capita income of " + selected_state + " is $" + average + ", and "
    elif the_data == 'Education':
        returned_string = "The average percentage of people with Bachelor's Degree or Higher in " + selected_state + " is " + average + "% , and "
    elif the_data == 'Homeownership':
        returned_string = "The homeownership rate of " + selected_state + " is " + average + "% , and "
    elif the_data == 'Employment':
        returned_string = "The average percentage increase of private non-farm employment in " + selected_state + " is " + average + "%, and "
    elif the_data == 'Diversity':
        returned_string = "The average percentage of people who are non-white (but including Hispanics and Latinos) in " + selected_state + " is " + average + "%, and "
    
    county_name = counties[0]["County"]
    county_data = 0
    if the_data == 'Income':
        for county in counties:
            if county["State"] == selected_state and county["Income"]["Per Capita Income"] > county_data:
                county_data = county["Income"]["Per Capita Income"]
                county_name = county["County"]
        return returned_string + county_name + " has the highest per capita income of " + selected_state + ": $" + str(county_data) 
    elif the_data == 'Education':
        for county in counties:
            if county["State"] == selected_state and county["Education"]["Bachelor's Degree or Higher"] > county_data:
                county_data = county["Education"]["Bachelor's Degree or Higher"]
                county_name = county["County"]
        return returned_string + county_name + " has the highest percentage of people with a Bachelor's Degree or Higher in " + selected_state + ": " + str(county_data) + "%"
    elif the_data == 'Homeownership':
        for county in counties:
            if county["State"] == selected_state and county["Housing"]["Homeownership Rate"] > county_data:
                county_data = county["Housing"]["Homeownership Rate"]
                county_name = county["County"]
        return returned_string + county_name + " has the highest homeownership rate in " + selected_state + ": " + str(county_data) + "%"
    elif the_data == 'Employment':
        for county in counties:
            if county["State"] == selected_state and county["Employment"]["Private Non-farm Employment Percent Change"] > county_data:
                county_data = county["Employment"]["Private Non-farm Employment Percent Change"]
                county_name = county["County"]
        return returned_string + county_name + " has the highest employment percentage increase in private non-farm businesses in " + selected_state + ": " + str(county_data) + "%"
    elif the_data == 'Diversity':
        county_data = 100.0
        for county in counties:
            if county["State"] == selected_state and county["Ethnicities"]["White Alone, not Hispanic or Latino"] < county_data:
                county_data = county["Ethnicities"]["White Alone, not Hispanic or Latino"]
                county_name = county["County"]
        county_data = 100.0 - county_data
        return returned_string + county_name + " has the highest non-white (but including Hispanics and Latinos) population percentage in " + selected_state + ": " + str(county_data) + "%"
    else:
        return ""

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
    school_percent = ""
    for county in counties:
        if county["County"] == county_select:
            percent = str(county["Education"]["High School or Higher"])
            school_percent = "In " + county_select + ", " + percent + "% have at least a high school education."
    return school_percent

if __name__=="__main__":
    app.run(debug=True)

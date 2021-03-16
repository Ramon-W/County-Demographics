from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html', response = get_state_options())

@app.route("/response")
def render_response():
    return render_template('response.html', fact = "cool")
    
    
    
    
    
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

if __name__=="__main__":
    app.run(debug=False)

from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

def main():
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)

def get_state_options():
    listOfStates = []
    htmlcode = ""
    for county in counties:
        if county["State"] not in listOfStates:
            state_dictionary.append(county["State"])
    return 

if __name__=="__main__":
    app.run(debug=False)

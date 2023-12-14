#!/usr/bin/env python3
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from pprint import pprint
import os

# app = Flask(__name__)  # , template_folder='../html')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores_db.sqlite3'
# db = SQLAlchemy(app)


# @app.route("/", methods=['GET', 'POST'])
def get_current_score(teams="Penguins"):

    score_data = requests.get('https://api-web.nhle.com/v1/score/now').json()

    return score_data


if __name__ == "__main__":
    print('\n*** Get Current Weather Conditions ***\n')

    teams = input("\nPlease enter a city name: ")

    score_data = get_current_score(teams)

    print("\n")
    pprint("This is score_data: {}".format(score_data))
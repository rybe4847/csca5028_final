import requests
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from score import get_current_score
import json
import os

# https://api.nhle.com/stats/rest
# https://api.nhle.com/stats/rest/en/game

# https://api-web.nhle.com/
# https://api-web.nhle.com/v1/score/now

app = Flask(__name__)  # , template_folder='../html')
app.config['SQLALCHEMY_DATABASE_URI'] = 'https://hockeystats-6920f95164aa.herokuapp.com'
db = SQLAlchemy(app)


class NHLGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    eastern_start_time = db.Column(db.DateTime)
    game_date = db.Column(db.Date)
    game_Number = db.Column(db.Integer)
    game_Schedule_State_Id = db.Column(db.Integer)
    game_State_Id = db.Column(db.Integer)
    game_Type = db.Column(db.Integer)
    home_Score = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer)
    period = db.Column(db.Integer)
    season = db.Column(db.Integer)
    visiting_team_id = db.Column(db.Integer)
    visiting_Score = db.Column(db.Integer)
    visiting_Team_Id = db.Column(db.Integer)

    def __repr__(self):
        return "<NHLGame {}>".format(self.id)


data_json = '''
{
    "data": [
        {
            "id": 1917020001,
            "easternStartTime": "1917-12-19T20:00:00",
            "gameDate": "1917-12-19",
            "gameNumber": 1,
            "gameScheduleStateId": 1,
            "gameStateId": 7,
            "gameType": 2,
            "homeScore": 4,
            "homeTeamId": 36,
            "period": 3,
            "season": 19171918,
            "visitingScore": 7,
            "visitingTeamId": 8
        }
    ]
}
'''


# Parse and save the game data to the database
@app.route('/')
def index():

    game_data = json.loads(data_json)['data'][0]

    # Convert the timestamp string to a Python datetime object
    timestamp_str = game_data['easternStartTime']
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')

    # Create an instance of NHLGame with the eastern_start_time field set
    new_game = NHLGame(
        game_id=game_data['id'],
        game_date=game_data['gameDate'],
        eastern_start_time=game_data['easternStartTime'],
        game_Number=game_data['gameNumber'],
        game_Schedule_State_Id=game_data['gameScheduleStateId'],
        game_State_Id=game_data['gameStateId'],
        game_Type=game_data['gameType'],
        home_Score=game_data['homeScore'],
        home_team_id=game_data['homeTeamId'],
        period=game_data['period'],
        season=game_data['season'],
        visiting_team_id=game_data['visitingTeamId'],
        visiting_Score=game_data['visitingScore'],
        visiting_Team_Id=game_data['visitingTeamId']
    )

    db.session.add(new_game)
    db.session.commit()

    return render_template('title.html')  # , focused_data=focused_data)







def get_data():
    response = requests.get("https://api.nhle.com/stats/rest/en/game")
    if response.status_code != 200:
        return "Failed to fetch data. Status Code: {}".format(response.status_code)
    else:
        return response.json()





# @app.route("/")
@app.route("/team_score", methods=['GET', 'POST'])  # This route handles form submission
def team_score():
    if request.method == 'POST':
        response = get_data()
        team_name = request.form.get('team')  # Get the name value of 'team' input from the form
        teams = request.args.get('team')
        score_data = get_current_score(teams)
        print("Team entered (team_name): {}".format(team_name), "-- Team entered (teams): {}".format(teams))
        # return "team_score() response json data: {}".format(get_data()['prevDate']))
    else:
        return "Method not allowed: {}".format(request.method)  # If accessed via GET (not through form submission)


@app.route("/league_score", methods=['GET', 'POST'])
def league_score():
    if request.method == 'POST':
        response = get_data()
        league_score_data = response  # Parse the JSON data from the response
        if "data" in league_score_data:
            i = 0
            data = league_score_data["data"]
            game_info = []
            for game in data:
                    date = game["gameDate"]
                    home_team = game["homeTeamId"]
                    away_team = game["visitingTeamId"]
                    # return "Date: {}".format(date), "Abbr: {}".format(day_abbrev), "NumGame: {}".format(num_of_games)
                    game_info.append((date, home_team, away_team))
                    print(i, date, home_team, away_team)
            return game_info

        else:
            return "data could not be fetched"


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8000)

import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_hackerrank_scores():
    url = "https://www.hackerrank.com/rest/contests/sd-challenge/leaderboard?offset=0&limit=1000&page%3A1"
    result = requests.get(url)
    leaderboard = json.loads(result.text)['models']

    score = {}

    for entry in leaderboard:
        score[entry['hacker']] = int(entry['score'])

    return score


def get_google_worksheet():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('SD Team-4cb745dfddbb.json', scope)
    gc = gspread.authorize(credentials)
    sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1z6pgqQEjsZ0_-oROpEpp_T4nmzIsq15ttQdO8MEgJI8/')
    worksheet = sht.get_worksheet(0)
    return worksheet


def update_scores():
    score = get_hackerrank_scores()
    worksheet = get_google_worksheet()

    for i in range(3, 127):
        username = worksheet.acell("D{}".format(i)).value
        if username in score:
            worksheet.update_acell("E{}".format(i), score[username])


update_scores()
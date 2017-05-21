import requests
import json
import gspread
import argparse
from oauth2client.service_account import ServiceAccountCredentials

URL_CHALLENGE = "https://www.hackerrank.com/rest/contests/sd-challenge/leaderboard?offset=0&limit=1000&page%3A1" 
URL_PARTIAL = "https://www.hackerrank.com/rest/contests/sd-test-practic-partial/leaderboard?offset=0&limit=1000&page%3A1"
URL_FINAL = "https://www.hackerrank.com/rest/contests/test-practic-final/leaderboard?offset=0&limit=1000&page%3A1"

ARGS = None


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Tool for extracting scores from Hackerrank Contests')
    parser.add_argument("--URL", dest="URL", type=str, default=URL_CHALLENGE)
    parser.add_argument("--username_column", dest="username_column", type=str, default="D")
    parser.add_argument("--dest_column", dest="dest_column", type=str, default="E")
    parser.add_argument("--multiplier", dest="multiplier", type=float, default=1)

    args = parser.parse_args()
    return args


def get_hackerrank_scores():
    url = ARGS.URL 
    result = requests.get(url)
    leaderboard = json.loads(result.text)['models']

    score = {}

    for entry in leaderboard:
        score[entry['hacker']] = int(entry['score']) * ARGS.multiplier

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

    for i in range(3, 131):
        username = worksheet.acell("{}{}".format(ARGS.username_column, i)).value
        print("#{}: {}".format(i, username))
        if username in score:
            worksheet.update_acell("{}{}".format(ARGS.dest_column, i), score[username])


if __name__ == "__main__":
    ARGS = parse_args()
    update_scores()

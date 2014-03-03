#!/usr/bin/python
import os, sys
sys.path.append(os.path.join(os.getcwd(), "soccer_night"))

import soccer_night
from getpass import getpass

def main():
    id = raw_input("Enter id: ")
    pw = getpass()

    soccer = soccer_night.SoccerNight(id, pw)

    while True:
        soccer.confirm_league_match_results()
        soccer.go_daily_match()

    soccer.close()
if __name__ == '__main__':
    main()

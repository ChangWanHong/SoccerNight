#!/usr/bin/python

import soccer_night
from getpass import getpass

def main():
    id = raw_input("Enter id: ")
    pw = getpass()

    soccer = soccer_night.SoccerNight(id, pw)

    while True:
        soccer.confirm_league_match_results()

    soccer.close()
if __name__ == '__main__':
    main()

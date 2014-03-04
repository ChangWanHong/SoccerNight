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
        soccer.challenge_to_friend_if_not_done()
        soccer.go_daily_match()
        soccer.go_world_tour()

    soccer.close()
if __name__ == '__main__':
    main()

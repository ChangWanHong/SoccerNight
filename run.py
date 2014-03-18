#!/usr/bin/python
import os, sys
sys.path.append(os.path.join(os.getcwd(), "soccer_night"))

import soccer_night
from getpass import getpass

def main():
    id = raw_input("Enter id: ")
    pw = getpass()
    pvp = raw_input("Enable pvp? [y/N]: ")

    soccer = soccer_night.SoccerNight(id, pw, pvp)

    while True:
        # reset state.
        soccer.reset_when_new_date()

        # functionality.
        soccer.challenge_to_friend_if_not_done()
        soccer.challenge_penalty_shoot_out()
        soccer.go_football_time()
        soccer.go_daily_match()
        soccer.go_football_time()
        soccer.go_world_tour()
        # Not work.
        #soccer.go_lineup()
        soccer.go_football_time()
        soccer.go_pvp()

    soccer.close()
if __name__ == '__main__':
    main()

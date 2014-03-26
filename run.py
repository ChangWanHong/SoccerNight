#!/usr/bin/python
import os, sys
sys.path.append(os.path.join(os.getcwd(), "soccer_night"))

import soccer_night
from getpass import getpass

def main():
    id = raw_input("Enter id: ")
    pw = getpass()
    pvp = raw_input("Enable pvp? [y/N]: ")
    print "** Using items. If you do not type and just enter, it doesn't work **"
    stamina = raw_input("Use strawberry gum? When? [0 ~ 100]: ")
    condition = raw_input("Use multi vitamin? How many do you want to fill? [1 ~ 5]: ")
    injury = raw_input("Use emergency kit? [y/N]: ")

    soccer = soccer_night.SoccerNight(id, pw, pvp, stamina, condition, injury)

    while True:
        # reset state.
        soccer.reset_when_new_date()

        soccer.go_item()

    soccer.close()
if __name__ == '__main__':
    main()

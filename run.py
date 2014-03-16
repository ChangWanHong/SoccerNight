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
        # reset state.
        soccer.reset_when_new_date()

        # functionality.
        soccer.go_lineup()

    soccer.close()
if __name__ == '__main__':
    main()

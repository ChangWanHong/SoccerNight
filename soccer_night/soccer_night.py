# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import re

IMPLICITLY_WAIT_SECONDS = 2
EXPLICITLY_WAIT_SECONDS = 5

class SoccerNight(object):

    driver = None
    wait = None

    day_of_week = None
    daily_match_remain = 5;
    world_tour_remain = 10;
    is_challenge_to_friend_done = False
    is_penalty_shoot_out_done = False
    pvp_remain = 10;
    user_want_to_pvp = False

    """ Caution!
    If we find element with find_elements_by_class_name, compound class names not permitted.
    So, *_CSS will be used with css selector frequently. It is reliable way.

    Sometimes, javascript execution will be needed. (*_JS)
    """
    # Common
    BUTTON_CHECK_RESULT_CLASS = "btn_ty3"
    POPUP_CONFIRM_ID = "a_popup_ok"
    BUTTON_ENTER_LIVE_LEAGUE_MATCH_CSS = ".btn_ty4"
    FINISH_LEAGUE_NEXT_PAGE_CSS = ".btn_p_pg2.nex"
    """ Get this with text. You get, for example, '/4' if you degrade from championship """
    FINISH_LEAGUE_REWARD_PLAYERS_YOU_CAN_CHOICE_XPATH = "//span[@class='num']/em"
    FINISH_LEAGUE_REWARD_PLAYERS_XPATH = "//ul[@class='reward_p_list _plist']/li"

    # Gifts and inventory
    GIFTS_YOU_GOT_CLASS = "thumb"
    BUTTON_GET_GIFT_ID = "gift_view_confirm_gift_button"
    BUTTON_UNPACK_INVENTORY_ITEM_ID = "unpack_button"
    BUTTON_CLOSE_WINDOW_UNPACKED_ITEM_CSS = ".btn_p_ty1.shop"

    # Daily match
    DAILY_MATCH_ACTIVATED_CSS = "._matchList"
    DAILY_MATCH_DISABLED_CSS = "._matchList.disb"
    BUTTON_RUN_DAILY_MATCH_CSS = ".sp_dm.btn_chall.ty2"

    # World tour
    BUTTON_WORLD_TOUR_NATION_IN_PROGRESS_CSS = ".over > span > a"
    BUTTON_RUN_WORLD_TOUR_ID = "a_wt_challengebtn"
    BUTTON_NATION_CLEAR_REWARD_CSS = ".btn_p_ty6._btnNationClear"

    # Friendly common
    GET_REWARD_BUTTON_AFTER_FRIENDLY_CLASS = "btn_p_ty6"
    BUTTON_QUIT_MATCH_CLASS = "btn_out"

    # In game
    MY_SCORE_JS = "return document.getElementsByClassName('score_r')[0].firstChild.firstChild.innerHTML"
    PC_SCORE_JS = "return document.getElementsByClassName('score_l')[0].firstChild.firstChild.innerHTML"
    PLAYING_TIME_XPATH = "//dl[@class='end_time']/dd"

    # Season results
    BUTTON_SEASON_RESULT_NEXT_CLASS = "btn_p_pg2 next"
    BUTTON_SEASON_RESULT_OK_CLASS = "btn_p_ty1 wd63"

    # Challenge to friend
    BUTTON_CHALLENGE_TO_FRIEND_CSS = "a.btn_game"
    BUTTON_CLOSE_FRIEND_LIST_CSS = "a._layer_close"
    BUTTON_OPEN_FRIEND_LIST_ID = "d_lnb_addfriend"
    CHALLENGE_TO_FRIEND_RESULT_POPUP_CONFIRM_ID = "challengeMatchOK"

    # Challenge to penalty shoot out
    BUTTON_NEXT_FRIEND_TO_SHOOT_OUT_ID = "head_shootout_btn"
    BUTTON_RUN_SHOOT_OUT_ID = "club_shootout_btn"
    NUMBER_REMAINED_FRIENDS_TO_SHOOT_OUT_CSS = "#head_shootout_btn > em"

    # PVP
    BUTTON_PVP_READY_CSS = ".btn_p_ty1.on"
    BUTTON_PVP_START_FASTLY_CSS = ".btn.start"
    BUTTON_PVP_MAKE_ROOM_CLASS = "btn_p_ty1"
    NUMBER_REMAINED_PVP_CSS = ".pvp_schedule > em > strong"

    def __init__(self, id, pw, pvp):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, EXPLICITLY_WAIT_SECONDS)
        self.driver.implicitly_wait(IMPLICITLY_WAIT_SECONDS)
        self.driver.get("http://fd.naver.com/gmc/main#home")

        elem = self.driver.find_element_by_id("id")
        elem.send_keys(id)
        elem = self.driver.find_element_by_id("pw")
        elem.send_keys(pw)
        elem.send_keys(Keys.ENTER)
        if pvp == "y" or pvp == "Y":
            self.user_want_to_pvp = True

        # There is new division for showing "This game is for older than 15".
        # This division blocks to click button for checking match results.
        time.sleep(6)
        self.__confirm_league_match_results()
        #TODO: Get reward from first login at home.

    def close(self):
        self.driver.close()

    def reset_when_new_date(self):
        if self.day_of_week == time.localtime().tm_wday:
            return

        self.day_of_week = time.localtime().tm_wday
        self.daily_match_remain = 5;
        self.world_tour_remain = 10;
        self.is_challenge_to_friend_done = False
        self.is_penalty_shoot_out_done = False
        self.pvp_remain = 10;

    def go_schedule(self, from_popup=False):
        if not from_popup:
            self.driver.get("http://fd.naver.com/gmc/main#schedule")
        else:
            try:
                self.wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, self.BUTTON_CHECK_RESULT_CLASS)))
            except:
                pass

        # For leeds time card.
        if self.__is_sunday():
            try:
                elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
            except:
                pass
            else:
                elem.click()

        check_buttons = self.driver.find_elements_by_class_name(self.BUTTON_CHECK_RESULT_CLASS)
        for check_button in check_buttons:
            check_button.click()

    def go_football_time(self):
        if not is_football_time():
            return

        self.go_schedule()
        try:
            elem = self.driver.find_element_by_css_selector(self.BUTTON_ENTER_LIVE_LEAGUE_MATCH_CSS)
        except:
            pass
        else:
            elem.click()

        # When it fails to enter live match.
        try:
            time.sleep(4)
            elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
            elem.click()
            self.go_football_time()
            return
        except:
            pass

        while True:
            # FIXME: It is difficult to catch popup.. Force to exit this loop.
            if time.localtime().tm_min >= 8:
                return
            # wait for game end and confirm popup
            try:
                elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
                elem.click()
                time.sleep(2)
                elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
                elem.click()
                time.sleep(2)
                elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
                elem.click()
            except:
                pass
            else:
                return

    def go_item(self):
        self.driver.get("http://fd.naver.com/gmc/main#item")
        #TODO: Use item properly.

    def go_gift(self):
        self.driver.get("http://fd.naver.com/gmc/main#gift")
        #TODO: Open presents.

    def go_storage(self):
        self.driver.get("http://fd.naver.com/gmc/main#storage")
        #TODO: Open given items.

    def go_daily_match(self):
        if self.daily_match_remain is 0:
            return

        self.driver.get("http://fd.naver.com/gmc/main#dailymatch")
        time.sleep(2)
        try:
            self.wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, self.DAILY_MATCH_ACTIVATED_CSS)))
            matches = self.driver.find_elements_by_css_selector(self.DAILY_MATCH_ACTIVATED_CSS)
            matches_disabled = self.driver.find_elements_by_css_selector(self.DAILY_MATCH_DISABLED_CSS)
            for disabled in matches_disabled:
                matches.remove(disabled)
        except:
            self.daily_match_remain = 0
            return
        else:
            self.daily_match_remain = len(matches)
            if self.daily_match_remain is 0:
                return

            for match in matches:
                match.click()
                self.driver.find_element_by_css_selector(self.BUTTON_RUN_DAILY_MATCH_CSS).click()
                self.driver.find_element_by_id(self.POPUP_CONFIRM_ID).click()
                if self.__confirm_league_match_results():
                    return

                while True:
                    playingTimeText = self.driver.find_element_by_xpath(self.PLAYING_TIME_XPATH).text
                    playingTime, _ = playingTimeText.split(":")
                    if int(playingTime) >= 89:
                        if not self.__is_my_score_more_than_pc(1):
                            # These clicks may not be needed because return statement makes it to enter daily match again.
                            self.driver.find_element_by_class_name(self.BUTTON_QUIT_MATCH_CLASS).click()
                            self.driver.find_element_by_id(self.POPUP_CONFIRM_ID).click()
                            return

                        if self.__confirm_friendly_match_result():
                            self.daily_match_remain -= 1
                            return

    def go_world_tour(self):
        if self.world_tour_remain is 0:
            return

        # Prevent alert. It was too fast.
        time.sleep(2)
        self.driver.get("http://fd.naver.com/gmc/main#worldtour")

        # At, not first time in world tour, the nation selection is skipped.
        # We are in page where club is chosen already.
        try:
            self.driver.find_element_by_css_selector(self.BUTTON_WORLD_TOUR_NATION_IN_PROGRESS_CSS).click()
        except:
            pass

        try:
            self.wait.until(expected_conditions.element_to_be_clickable((By.ID, self.BUTTON_RUN_WORLD_TOUR_ID)))
            button_run = self.driver.find_element_by_id(self.BUTTON_RUN_WORLD_TOUR_ID)
        except:
            self.world_tour_remain = 0
            return
        else:
            button_run.click()
            self.driver.find_element_by_id(self.POPUP_CONFIRM_ID).click()

        if self.__confirm_league_match_results():
            return

        while True:
            playingTimeText = self.driver.find_element_by_xpath(self.PLAYING_TIME_XPATH).text
            playingTime, _ = playingTimeText.split(":")
            if int(playingTime) >= 89:
                if not self.__is_my_score_more_than_pc(3):
                    # These clicks may not be needed because return statement makes it to enter world tour again.
                    self.driver.find_element_by_class_name(self.BUTTON_QUIT_MATCH_CLASS).click()
                    self.driver.find_element_by_id(self.POPUP_CONFIRM_ID).click()
                    return

                if self.__confirm_friendly_match_result():
                    self.daily_match_remain -= 1
                    # For next nation popup. Reward for clearing nation.
                    try:
                        time.sleep(2)
                        self.wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, self.BUTTON_NATION_CLEAR_REWARD_CSS)))
                        elem = self.driver.find_element_by_css_selector(self.BUTTON_NATION_CLEAR_REWARD_CSS)
                        elem.click()
                        elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
                        elem.click()
                    except:
                        pass

                    return

    def challenge_to_friend_if_not_done(self):
        if self.is_challenge_to_friend_done:
            return

        elem = self.driver.find_element_by_id(self.BUTTON_OPEN_FRIEND_LIST_ID)
        elem.click()

        # LIMIT: Arbitrary number expected to exceed the number of friends of
        # any user, which prevents an infinite while loop on worst, unexpected cases.
        LIMIT = 100
        index = 0
        while index < LIMIT:
            # Prevent from popup which is shown when many requests send to server in short time.
            time.sleep(1)
            try:
                elem = self.driver.find_element_by_css_selector(self.BUTTON_CHALLENGE_TO_FRIEND_CSS)
                elem.click()
            except NoSuchElementException:
                elem = self.driver.find_element_by_css_selector(self.BUTTON_CLOSE_FRIEND_LIST_CSS)
                elem.click()
                self.is_challenge_to_friend_done = True
                return
            except:
                return

            try:
                self.wait.until(expected_conditions.element_to_be_clickable((By.ID, self.CHALLENGE_TO_FRIEND_RESULT_POPUP_CONFIRM_ID)))
                elem = self.driver.find_element_by_id(self.CHALLENGE_TO_FRIEND_RESULT_POPUP_CONFIRM_ID)
                elem.click()
            except:
                return
            index += 1

    def challenge_penalty_shoot_out(self):
        if self.is_penalty_shoot_out_done:
            return

        while not self.is_penalty_shoot_out_done:
            self.driver.get("http://fd.naver.com/club")
            remained_string = self.driver.find_element_by_css_selector(self.NUMBER_REMAINED_FRIENDS_TO_SHOOT_OUT_CSS).text
            remained, _ = map(int, re.findall(r'\d+', remained_string))

            if remained is 0:
                self.is_penalty_shoot_out_done = True
                return

            try:
                self.driver.find_element_by_id(self.BUTTON_NEXT_FRIEND_TO_SHOOT_OUT_ID).click()
                self.driver.find_element_by_id(self.BUTTON_RUN_SHOOT_OUT_ID).click()
                time.sleep(1.5)
            except:
                pass

    def go_pvp(self):
        if (not self.user_want_to_pvp or self.daily_match_remain or self.world_tour_remain
            or not self.is_challenge_to_friend_done or not self.is_penalty_shoot_out_done
            or not self.pvp_remain):
            return

        self.driver.get("http://fd.naver.com/gmc/main#pvp")
        self.pvp_remain = int(self.driver.find_element_by_css_selector(self.NUMBER_REMAINED_PVP_CSS).text)
        if self.pvp_remain is 0:
            return

        time.sleep(1)
        try:
            elem = self.driver.find_element_by_css_selector(self.BUTTON_PVP_START_FASTLY_CSS)
            elem.click()
            time.sleep(1)
            elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
            elem.click()
        except:
            return
        else:
            if self.__confirm_friendly_match_result():
                return

            time.sleep(1)
            # Ready.
            try:
                elem = self.driver.find_element_by_css_selector(self.BUTTON_PVP_READY_CSS)
                elem.click()
            except:
                # Make room
                try:
                    elem = self.driver.find_element_by_class(self.BUTTON_PVP_MAKE_ROOM_CLASS)
                    elem.click()
                except:
                    # If you fail to enter.
                    elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
                    elem.click()
                    return
                else:
                    # Speculation time for making room and game.
                    time.sleep(12)
                    # Anyway, we do nothing here because game is started and
                    # then you can out from game automatically.

            # Play the pvp. Assume playing time is 8 mins and 20 secs. And wait
            # to counterpart ready for 20 secs.
            else:
                time.sleep(8 * 60 + 40)


    # It will be used densly..
    def __confirm_league_match_results(self):
        try:
            elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
        except:
            return False
        else:
            elem.click()
            self.go_schedule(True)
            return True

    def __confirm_friendly_match_result(self):
        try:
            elem = self.driver.find_element_by_class_name(self.GET_REWARD_BUTTON_AFTER_FRIENDLY_CLASS)
            elem.click()
            elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
            elem.click()
        except:
            return False
        else:
            return True

    def __is_my_score_more_than_pc(self, difference):
        me = int(self.driver.execute_script(self.MY_SCORE_JS))
        pc = int(self.driver.execute_script(self.PC_SCORE_JS))
        return me >= pc + difference

    # For leeds time card
    def __is_sunday(self):
        return self.day_of_week == 6

# Utilities. static method.
def is_football_time():
    # We enter football time during "13:55 ~ 14:05" and "21:55 ~ 22:05".
    # because the longest time of a functionality is in the match. We assume
    # it's 7 minutes.
    if (((time.localtime().tm_hour is 14 and time.localtime().tm_min < 5)
        or (time.localtime().tm_hour is 13 and time.localtime().tm_min > 55))
        or ((time.localtime().tm_hour is 22 and time.localtime().tm_min < 5)
        or (time.localtime().tm_hour is 21 and time.localtime().tm_min > 55))):
        return True

    return False


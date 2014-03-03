# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

IMPLICITLY_WAIT_SECONDS = 2

class SoccerNight(object):

    driver = None
    wait = None
    daily_match_remain = 5;
    world_tour_remain = 10;

    """ Caution!
    If we find element with find_elements_by_class_name, compound class names not permitted.
    So, FRIENDLY_ACTIVE_MATCH_CSS will be used with css selector. It is reliable way.

    Sometimes, javascript execution will be needed.
    """
    # Common
    BUTTON_CHECK_RESULT_CLASS = "btn_ty3"
    POPUP_CONFIRM_ID = "a_popup_ok"

    # Daily match
    DAILY_MATCH_ACTIVATED_CSS = "._matchList"
    DAILY_MATCH_DISABLED_CSS = "._matchList.disb"
    DAILY_MATCH_LAST_DISABLED_CSS = "._matchList.last.disb"
    BUTTON_RUN_DAILY_MATCH_CSS = ".sp_dm.btn_chall.ty2"

    # World tour
    BUTTON_RUN_WORLD_TOUR_CSS = ".sp_dm.btn_chall"

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
    CHALLENGE_FRIEND_CLASS = "rst clg"


    def __init__(self, id, pw):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(IMPLICITLY_WAIT_SECONDS)
        self.driver.get("http://fd.naver.com/gmc/main#home")

        elem = self.driver.find_element_by_id("id")
        elem.send_keys(id)
        elem = self.driver.find_element_by_id("pw")
        elem.send_keys(pw)
        elem.send_keys(Keys.ENTER)

        #TODO: Get reward from first login at home.

    def close(self):
        self.driver.close()

    def go_schedule(self, from_popup=False):
        if not from_popup:
            self.driver.get("http://fd.naver.com/gmc/main#schedule")
        else:
            self.wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, self.BUTTON_CHECK_RESULT_CLASS)))

        # For leeds time card.
        if (self.__is_sunday()):
            try:
                elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_ID)
            except:
                pass
            else:
                elem.click()

        check_buttons = self.driver.find_elements_by_class_name(self.BUTTON_CHECK_RESULT_CLASS)
        for check_button in check_buttons:
            check_button.click()

        #TODO: Foot ball time.

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
        # FIXME: At 24 o'clock, we should refresh this.
        if (self.daily_match_remain == 0):
            return

        self.driver.get("http://fd.naver.com/gmc/main#dailymatch")
        try:
            self.wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, self.DAILY_MATCH_ACTIVATED_CSS)))
            matches = self.driver.find_elements_by_css_selector(self.DAILY_MATCH_ACTIVATED_CSS)
            matches_disabled = self.driver.find_elements_by_css_selector(self.DAILY_MATCH_DISABLED_CSS)
            matches_disabled_last = self.driver.find_elements_by_css_selector(self.DAILY_MATCH_LAST_DISABLED_CSS)
            for disabled in matches_disabled:
                matches.remove(disabled)
            for disabled in matches_disabled_last:
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
                if (self.confirm_league_match_results()):
                    return

                while True:
                    playingTimeText = self.driver.find_element_by_xpath(self.PLAYING_TIME_XPATH).text
                    playingTime, _ = playingTimeText.split(":")
                    me = int(self.driver.execute_script(self.MY_SCORE_JS))
                    pc = int(self.driver.execute_script(self.PC_SCORE_JS))
                    if (int(playingTime) > 90):
                        if (not self.__is_my_score_more_than_pc(1)):
                            self.driver.find_element_by_class_name(self.BUTTON_QUIT_MATCH_CLASS)
                            return

                        if (self.__confirm_friendly_match_result()):
                            self.daily_match_remain -= 1
                            return

    def go_world_tour(self):
        # FIXME: At 24 o'clock, we should refresh this.
        if (self.world_tour_remain == 0):
            return

        self.driver.get("http://fd.naver.com/gmc/main#worldtour")
        #self.driver.find_element_by_xpath("//div[@class='over']/span/a").click()
        self.driver.find_element_by_css_selector(".over > span > a").click()
        self.world_tour_remain = 0
        #TODO: Start world tour.

    # It will be used densly..
    def confirm_league_match_results(self):
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
        return time.localtime().tm_wday == 6


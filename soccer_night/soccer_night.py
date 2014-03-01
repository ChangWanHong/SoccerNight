# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class SoccerNight(object):

    driver = None

    BUTTON_CHECK_RESULT_CLASS = "btn_ty3"
    POPUP_CONFIRM_RESULT_ID = "a_popup_ok"

    FRIENDLY_ACTIVE_MATCH_CLASS = "_matchList"
    BUTTON_RUN_FRIENDLY_MATCH_CLASS = "sp_dm btn_chall ty2"
    MY_SCORE_XPATH = "//dd[@class='score_r']/span/span"
    PC_SCORE_XPATH = "//dd[@class='score_l']/span/span"
    PLAYING_TIME_XPATH = "//dl[@class='end_time']/dd"
    BUTTON_QUIT_MATCH_CLASS = "btn_out"
    GET_REWARD_BUTTON_AFTER_FRIENDLY_CLASS = "btn_p_ty6"

    def __init__(self, id, pw):
        self.driver = webdriver.Chrome()
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
            wait = WebDriverWait(self.driver, 10)
            wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, self.BUTTON_CHECK_RESULT_CLASS)))

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
        self.driver.get("http://fd.naver.com/gmc/main#dailymatch")
        #TODO: Start daily match.

    def go_world_tour(self):
        self.driver.get("http://fd.naver.com/gmc/main#worldtour")
        #TODO: Start world tour.

    def confirm_league_match_results(self):
        try:
            elem = self.driver.find_element_by_id(self.POPUP_CONFIRM_RESULT_ID)
        except:
            pass
        else:
            elem.click()
            self.go_schedule(True)


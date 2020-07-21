# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re
import pyautogui
import os
up = os.environ.get('USERPROFILE')

ChromePath = '--user-data-dir=' + up + '\\AppData\\Local\\Google\\Chrome\\User Data\\'


def FindImg(imageName):
    imageOnScreen = pyautogui.locateOnScreen(imageName)
    if imageOnScreen is not None:
        print('%s Found on screen' % imageName)
        return imageOnScreen
    else:
        print('%s Not Found on screen' % imageName)
        return False


class GooglePhotosDataUpdater(unittest.TestCase):
    def setUp(self):
        # Chrome Setup - Make sure Chrome is already not running!
        chromedriver = up + "/chromedriver.exe"

        options = webdriver.ChromeOptions()
        # Path to your chrome profile
        options.add_argument(ChromePath)
        self.driver = webdriver.Chrome(chrome_options=options,
                                       executable_path=chromedriver)
        # self.driver = webdriver.Firefox()
        print("Chrome Launched!")

        self.driver.implicitly_wait(30)
        self.base_url = "https://photos.google.com/photo/***********"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_google_photos_data_updater(self):
        driver = self.driver
        driver.get(self.base_url)

        def DoThis():
            driver.refresh()
            pyautogui.moveTo(1200, 90)
            time.sleep(1)
            pyautogui.click()

            ImgName = driver.find_element_by_xpath("//*[contains(@aria-label,'Filename:')]").text

            print(ImgName)
            if '2015' in ImgName.split('-')[1]:
                year = '2015'
            elif '2016' in ImgName.split('-')[1]:
                year = '2016'
            elif '2017' in ImgName.split('-')[1]:
                year = '2017'
            month = ImgName.split('-')[1][4:6]
            day = ImgName.split('-')[1][6:8]
            if year is not None:
                if month is not None:
                    if day is not None:
                        pyautogui.moveTo(1143, 310)
                        time.sleep(1)
                        pyautogui.click()
                        time.sleep(1)

                        driver.find_element_by_xpath('//input[@aria-label="Year"]').click()
                        driver.find_element_by_xpath('//input[@aria-label="Year"]').clear()
                        driver.find_element_by_xpath('//input[@aria-label="Year"]').send_keys(year)

                        driver.find_element_by_xpath('//input[@aria-label="Month"]').clear()
                        driver.find_element_by_xpath('//input[@aria-label="Month"]').send_keys(month)

                        driver.find_element_by_xpath('//input[@aria-label="Day"]').clear()
                        driver.find_element_by_xpath('//input[@aria-label="Day"]').send_keys(day)

                        time.sleep(0.5)
                        pyautogui.moveTo(755, 533)
                        pyautogui.click()
                        time.sleep(2)

        for i in range(0, 200):
            try:
                DoThis()
            except:
                pass
            pyautogui.moveTo(948, 525)
            pyautogui.click()
            time.sleep(1)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()

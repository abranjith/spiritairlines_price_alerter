'''
__author__ = 'Ranjith'

This script is based on base page object design patter common in selenium framework creation.
Each page is viewed as a class and hosts all elements and functionalities that a particular page provides.
This can be imported and used by tests

'''

from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class  BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def convert_this_type(self, locator_type):
        if locator_type.upper() == "ID":
            return By.ID
        elif locator_type.upper() == "NAME":
            return By.NAME
        elif locator_type.upper() == "XPATH":
            return By.XPATH
        elif locator_type.upper() == "LINK_TEXT":
            return By.LINK_TEXT
        elif locator_type.upper() == "PARTIAL_LINK_TEXT":
            return By.PARTIAL_LINK_TEXT
        elif locator_type.upper() == "TAG_NAME":
            return By.TAG_NAME

    def is_element_present(self, locator_value, locator_type="ID"):

        loc_type = self.convert_this_type(locator_type)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((loc_type, locator_value))
            )
            return True

        except TimeoutException as e:
            return False

    def find_element_withpatience(self, locator_value, locator_type="ID", waittime=10):

        loc_type = self.convert_this_type(locator_type)

        try:
            element = WebDriverWait(self.driver, waittime).until(
                EC.presence_of_element_located((loc_type, locator_value))
            )
            return element

        except TimeoutException as e:
            raise NoSuchElementException

    def find_next_element(self, element):

        return element.find_element_by_xpath("following-sibling::em")

    def find_elements_withpatience(self, locator_value, locator_type="ID", waittime=10):

        loc_type = self.convert_this_type(locator_type)

        try:
            elements = WebDriverWait(self.driver, waittime).until(
                EC.presence_of_all_elements_located((loc_type, locator_value))
            )
            return elements

        except TimeoutException as e:
            raise NoSuchElementException

class  MainPage(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        assert self.is_element_present("flightOnlyWidgetOptions"), "Couldn't locate main page"

        self.link_flight = self.find_element_withpatience("flightOnlyWidgetOptions")

    def click_flight(self):
        self.link_flight.click()

class  FormPage(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        assert self.is_element_present("departCityCodeSelect"), "Couldn't locate form page"

        self.select_from = Select(self.find_element_withpatience("departCityCodeSelect"))
        self.select_to = Select(self.find_element_withpatience("destCityCodeSelect"))
        self.depart_date = self.find_element_withpatience("departDate")
        self.return_date = self.find_element_withpatience("returnDate")
        self.btn_submit = self.find_element_withpatience("//*[@id='book-travel-form']/p/button", locator_type="xpath")

    def enter_from(self, start_from):
        #self.select_from.select_by_visible_text(start_from)
        self.select_from.select_by_value(start_from)

    def enter_to(self, dest_to):
        #self.select_to.select_by_visible_text(dest_to)
        self.select_to.select_by_value(dest_to)

    def enter_depart_date(self, depart_date):
        self.depart_date.clear()
        self.depart_date.send_keys(depart_date)

    def enter_return_date(self, return_date):
        self.return_date.clear()
        self.return_date.send_keys(return_date)

    def submit_form(self):
        self.btn_submit.submit()


class ResultPage(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def get_min_departure_price(self):
        depart_radios = self.find_elements_withpatience("//*[@type='radio']", locator_type="XPATH")

        for rad in depart_radios:
            id = rad.get_attribute("name")

            if id:
                if "Market1" in id and rad.is_selected():
                    return rad.find_element_by_xpath("following-sibling::em").text

    def get_min_arrival_price(self):
        depart_radios = self.find_elements_withpatience("//*[@type='radio']", locator_type="XPATH")

        for rad in depart_radios:
            id = rad.get_attribute("name")

            if id:
                if "Market2" in id and rad.is_selected():
                    return rad.find_element_by_xpath("following-sibling::em").text

if __name__ == '__main__':
    pass
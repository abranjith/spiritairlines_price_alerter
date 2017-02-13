'''
__author__ = 'Ranjith'
This script actually crawls through the website to fetch actual data and message to the user
Make sure to configure Config.txt before using
'''
import ConfigParser
import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from spirit_pages import *

from twilio.rest import TwilioRestClient
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

def main():

    #read schedule interval data
    daily_schedule_hours = config_parser.get("SCHEDULE_SECTION", "daily_schedule_hours")

    #scheduler to run this program
    sched = BlockingScheduler()
    sched.add_job(looper, 'cron', hour=daily_schedule_hours)
    sched.start()

    #looper() #makes direct call once


def looper():

    #read parameters to enter on the website
    url = config_parser.get("SPIRIT_SECTION", "url")
    from_airport, to_airport = [c.strip() for c in config_parser.get("SPIRIT_SECTION", "from_to_airports").split("-")]
    from_to_dates = [d.split("-") for d in config_parser.get("SPIRIT_SECTION", "from_to_dates").split(";")]

    final_msg = "@" + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f") + "\n"
    for from_date, to_date in from_to_dates:
        #options for the chrome webdriver
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36")
        opts.add_argument("disable-popup-blocking")

        driver = webdriver.Chrome(chrome_options=opts)

        try:
            driver.get(url)
            #visit again to get rid of popup
            driver.get(url)

            main_page = MainPage(driver)
            main_page.click_flight()

            #enter airport, dates and submit form
            form_page = FormPage(driver)
            form_page.enter_from(from_airport)
            form_page.enter_to(to_airport)
            form_page.enter_depart_date(from_date)
            form_page.enter_return_date(to_date)
            form_page.submit_form()

            #print driver.page_source
            result_page = ResultPage(driver)
            dep_price = result_page.get_min_departure_price()
            ret_price = result_page.get_min_arrival_price()

            final_msg += "Depart = %s for %s\nReturn = %s for %s\n\n" %(from_date, dep_price, to_date, ret_price)

        except Exception as e:
            logger.error(e.message)

        finally:
            driver.close()
            driver.quit()

    #send sms
    send_sms(final_msg)

    #also log
    logger.info(final_msg)

def send_sms(message):
    #read parameters that is needed to send sms
    from_number = config_parser.get("SMS_SECTION", "from_number")
    to_number = config_parser.get("SMS_SECTION", "to_number")
    twilio_account_number = config_parser.get("SMS_SECTION", "twilio_account_number")
    twilio_account_token = config_parser.get("SMS_SECTION", "twilio_account_token")

    client = TwilioRestClient(twilio_account_number, twilio_account_token)
    client.messages.create(to=to_number, from_=from_number,
                        body=message)


if __name__ == '__main__':
    #read and initialize from config
    config_file = os.path.join(os.path.pardir, "config", "Config.txt")
    config_parser = ConfigParser.RawConfigParser()
    config_parser.read(config_file)

    #initialize logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler(os.path.join(os.path.pardir, "log", "logger.log"))
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    main()

# spiritairlines_price_alerter
A tool that scans the current price for user given location and dates and sends text message

PREREQUISITE:-
Python - You will need python 2.7. 
This has been built and tested on python version 2.7 and Windows OS using Selenium webdriver. You will need some modifications in case you are using python 3.x

Twilio account - You will need twilio account for messaging. It is easy to get one and it's free. Check it out !!

External libraries - This tool uses some external packages. Please install packages per requirements.txt. If you are using different versions of packages than the ones mentioned, it might require some thorough testing
This tool uses Chrome browser. Make sure chromedriver(for selenium) is in your PATH

Use the same folder structure as in the project

CONFIGURATION:-
Before running the program, make sure to update Config.txt under config directory
SPIRIT_SECTION - You can keep the url. Feel free to update airport information and dates. This tool runs through all the dates mentioned here (from and to dates are separated by "-" and multiple dates are separated by ";"). Make sure dates are >= current date

SMS_SECTION - Your twilio account information goes here

SCHEDULE_SECTION - once you trigger the script, it runs daily and sends message at the exact hours mentioned (in 24 hour format)

RUN:-
Execute crawler.py (with command prompt you would enter- python crawler.py)
You can also schedule crawler.py as a task that is executed by your OS



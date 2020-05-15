import re
import sys
import time
from configparser import ConfigParser

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

config = ConfigParser()
config.read('config.ini')

USERNAME = config.get('codewars', 'username')
email = config.get('codewars', 'email')
password = config.get('codewars', 'password')

browser = config.get('settings', 'browser')
scroll_delay = int(config.get('settings', 'scroll_delay'))

SIGNIN_URL = 'https://www.codewars.com/users/sign_in'
SOLUTIONS_URL = 'https://www.codewars.com/users/{}/completed_solutions'.format(USERNAME)

drivers = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
}


def download_source():
    try:
        driver = drivers[browser]()
    except WebDriverException as e:
        print('Driver for {} is missing!'.format(browser))
        print('Exception {}'.format(e))
        sys.exit(1)

    driver.get(SIGNIN_URL)

    # login
    email_input = driver.find_element_by_name('user[email]')
    email_input.clear()
    email_input.send_keys(email)

    password_input = driver.find_element_by_name('user[password]')
    password_input.clear()
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # going to solutions page
    driver.get(SOLUTIONS_URL)

    # finds the number of completed challenges. Each page contains 15 challenges
    elem_completed = driver.find_elements_by_xpath(
        "//*[contains(text(), 'Completed')]")[0].text
    completed_challenges = int(re.search('Completed \((\d*)\)', elem_completed).group(1))
    times_scroll = completed_challenges // 15

    # scrolling the page to get all challenges
    for i in range(times_scroll):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_delay)

    with open('./challenges.html', 'w') as file:
        file.write(driver.page_source)

    driver.close()

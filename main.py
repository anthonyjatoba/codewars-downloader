import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# TODO property with user's browser/driver
driver = webdriver.Chrome()

# TODO see if user is already logged in
driver.get('https://www.codewars.com/users/sign_in')

# TODO use json config file
USERNAME = 
EMAIL = 
PASSWORD = 

# login
email_input = driver.find_element_by_name('user[email]')
email_input.clear()
email_input.send_keys(EMAIL)

password_input = driver.find_element_by_name('user[password]')
password_input.clear()
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.RETURN)

# going to solutions page
driver.get('https://www.codewars.com/users/{}/completed_solutions'.format(USERNAME))

# finds the number of completed challenges. Each page contains 15 challenges
elem_completed = driver.find_elements_by_xpath("//*[contains(text(), 'Completed')]")[0].text
completed = int(re.search('Completed \((\d*)\)', elem_completed).group(1))
n_scroll = completed // 15

# scrolling the page to get all challenges
for i in tqdm(range(n_scroll)):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

with open('./challenges.html', 'w') as file:
    file.write(driver.page_source)

driver.close()
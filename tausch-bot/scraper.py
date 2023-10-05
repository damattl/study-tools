import os

import dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from scraper_utils import login, parse_table, go_to_course_site, add_attendance_info

dotenv.load_dotenv()

base_url = "https://imed-campus.uke.uni-hamburg.de"

browser = webdriver.Firefox()
browser.get(f"{base_url}/startseite")

login(browser, os.environ["USERNAME"], os.environ["PASSWORD"])
browser.get(f"{base_url}/stundenplan")

select_weeks_element = browser.find_element(By.CSS_SELECTOR,
                                            "#c525 > form > table > tbody > tr > td:nth-child(5) > select:nth-child(2)")
select_weeks = Select(select_weeks_element)

select_weeks.select_by_value("7")

select_view_mode_element = browser.find_element(By.CSS_SELECTOR,
                                                "#c525 > form > table > tbody > tr > td:nth-child(5) > select:nth-child(1)")
select_view_mode = Select(select_view_mode_element)

select_view_mode.select_by_value("1")

table = browser.find_element(By.CSS_SELECTOR, "#ttab")
parsed = parse_table(table)
print(parsed)

for course in parsed:
    go_to_course_site(browser, base_url, course)
    add_attendance_info(browser, course)

print(parsed)

# TODO: Get swap options
# TODO: Get exchange options

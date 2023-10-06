import os

import dotenv
from selenium import webdriver

import scraper_utils


dotenv.load_dotenv()

base_url = "https://imed-campus.uke.uni-hamburg.de"

browser = webdriver.Firefox()
browser.get(f"{base_url}/startseite")

scraper_utils.login(browser, os.environ["USERNAME"], os.environ["PASSWORD"])
browser.get(f"{base_url}/stundenplan")

raw_courses = scraper_utils.scrape_all_weeks(browser)


courses = []
for course_dict in raw_courses:
    scraper_utils.go_to_course_site(browser, base_url, course_dict)
    course = scraper_utils.create_course_object(browser, course_dict)
    print(course.__str__())
    courses.append(course)

print(courses)

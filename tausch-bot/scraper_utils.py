from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from models import SwapOption, Course


def login(browser: WebDriver, username: str, password: str):
    username_field = browser.find_element(By.CSS_SELECTOR, "#benutzername")
    pass_field = browser.find_element(By.CSS_SELECTOR, "#kennwort")

    login_button = browser.find_element(By.CSS_SELECTOR,
                                        "body > div > div.header > div.part1 > div > div > form > p > input.login-button")

    username_field.send_keys(username)
    pass_field.send_keys(password)  # TODO: NEVER COMMIT

    login_button.click()
    print(login_button)
    print(username_field)
    print(pass_field)


def parse_table(table: WebElement) -> list[dict[str, str]]:
    parsed_table = []

    for row in table.find_elements(By.TAG_NAME, 'tr'):
        cells = row.find_elements(By.TAG_NAME, 'td')
        parsed = []
        for cell in cells:
            parsed.append(cell.text)
        parsed_table.append(parsed)

    table_header = parsed_table[0]

    courses = []
    for row in parsed_table[1:]:
        row_dict: dict[str, str] = {}
        for i in range(len(table_header)):
            row_dict[table_header[i]] = row[i]
        courses.append(row_dict)

    return courses


def go_to_course_site(browser: WebDriver, base_url: str, course_dict: dict[str, str]):
    path = f"/stundenplan?cid={course_dict['Cid']}"
    browser.get(f"{base_url}{path}")


def create_course_object(browser: WebDriver, course_dict: dict[str, any]) -> Course:
    info_table = browser.find_element(By.CSS_SELECTOR, "#c533 > fieldset:nth-child(1) > table")
    rows = info_table.find_elements(By.TAG_NAME, "tr")

    return Course(course_dict, parse_attendance_info(rows[-1].text), get_swap_options(browser))


def parse_attendance_info(raw: str):
    if raw.find("ohne elektr. Anwesenheitskontrolle") != -1:
        return 0
    return int(raw.split("//")[-1].replace("Anw.Pkt.", "").strip())


def get_swap_options(browser: WebDriver):
    try:
        select_button = browser.find_element(By.CSS_SELECTOR, "#c533 > fieldset:nth-child(2) > form > table > tbody > tr:nth-child(6) > th > select")
    except:
        return

    select = Select(select_button)

    options = []
    for item in select.options:
        option = parse_option(item)
        print(option.__str__())
        if option is None:
            continue
        options.append(option)
    return options


def parse_option(option: WebElement) -> Optional[SwapOption]:
    value = option.get_attribute("value")
    if value is None or value is "":
        return None

    print(value)
    print(option.text.split("//"))
    split_once = option.text.split("//")
    split_twice = []
    for item in split_once:
        split_twice.extend(item.split("/"))

    return SwapOption(value, split_twice)


def scrape_all_weeks(browser: WebDriver) -> list[dict[str, str]]:
    courses = []
    while True:
        select_weeks_element = browser.find_element(By.CSS_SELECTOR,
                                                    "#c525 > form > table > tbody > tr > td:nth-child(5) > select:nth-child(2)")
        select_weeks = Select(select_weeks_element)
        select_weeks.select_by_value("1")

        select_view_mode_element = browser.find_element(By.CSS_SELECTOR,
                                                        "#c525 > form > table > tbody > tr > td:nth-child(5) > select:nth-child(1)")

        select_view_mode = Select(select_view_mode_element)
        select_view_mode.select_by_value("1")

        scraped_courses = scrape_week(browser)

        if len(scraped_courses) == 0 and len(courses) != 0:
            break

        courses.extend(scraped_courses)
        next_week_button = browser.find_element(By.CSS_SELECTOR,
                                                "#c525 > form > table > tbody > tr > td:nth-child(3) > input[type=submit]")

        next_week_button.click()

    return courses


def scrape_week(browser: WebDriver) -> list[dict[str, str]]:
    table = browser.find_element(By.CSS_SELECTOR, "#ttab")
    parsed = parse_table(table)
    return parsed


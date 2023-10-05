from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


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


def add_attendance_info(browser: WebDriver, course_dict: dict[str, str]):
    info_table = browser.find_element(By.CSS_SELECTOR, "#c533 > fieldset:nth-child(1) > table")
    rows = info_table.find_elements(By.TAG_NAME, "tr")
    course_dict["Anwesenheit"] = rows[-1].text

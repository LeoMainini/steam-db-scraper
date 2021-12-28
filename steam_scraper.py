from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import os
from time import sleep


class SteamScraper():

    def __init__(self, url):
        self.url = url
        service = Service(os.environ.get("CHROME_DRIVER_PATH"))
        self.driver: WebDriver = Chrome(service=service)

    def get_tables(self) -> list[WebElement]:
        self.driver.get(self.url)
        sleep(1)
        tables: list[WebElement] = self.driver.find_elements(
            By.CLASS_NAME, "table-products")

        return tables

    def process_table_data(self):
        tables = {}
        table_data = self.get_tables()
        for table in table_data:

            columns: list[WebElement] = table.find_elements(By.TAG_NAME, "th")
            column_titles = [column.text for column in columns]
            if 'Last 7 days' in column_titles:
                column_titles.pop(column_titles.index('Last 7 days'))
            if table == table_data[0]:
                apps = table.find_elements(By.CSS_SELECTOR, "tr.app")
                apps = apps[1:]
            else:
                apps: list[WebElement] = table.find_elements(
                    By.CSS_SELECTOR, "tr.app")

            app_titles = [app.find_element(
                By.CLASS_NAME, 'css-truncate').text for app in apps]
            all_apps_data = [app.find_elements(
                By.CLASS_NAME, 'text-center') for app in apps]
            for i in range(len(column_titles[1:])):
                if len(column_titles) > 2:
                    tables[column_titles[0]] = {
                        "Title": app_titles,
                        column_titles[1]: [app_data[0].text for app_data in all_apps_data],
                        column_titles[2]: [
                            app_data[1].text for app_data in all_apps_data]
                    }
                else:
                    tables[column_titles[0]] = {
                        "Title": app_titles,
                        column_titles[1]: [
                            app_data[0].text for app_data in all_apps_data]
                    }
        self.driver.close()
        return tables

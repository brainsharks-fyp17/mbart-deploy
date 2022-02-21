import os
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# from dotenv import load_dotenv
# load_dotenv()

base_url = "http://localhost:5000"

service = Service(ChromeDriverManager().install())
input_output_mapping = {

}


def send_input(driver, input_output):
    print("BASE URL: ", base_url)
    driver.get(base_url)
    driver.find_element(By.CLASS_NAME, "input_text").find_element(By.TAG_NAME, "textarea"). \
        send_keys("Text input")
    # print(elements)
    # elements[0].send_keys("Text input")
    # driver.find_element(By.CLASS_NAME, 'username').send_keys(username)
    # driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'panel_button submit').click()


class TestInput:
    def test_login_success(self):
        print("BASE URL: ", base_url)
        driver = webdriver.Chrome(service=service)
        try:
            send_input(driver, input_output_mapping)
        finally:
            driver.quit()

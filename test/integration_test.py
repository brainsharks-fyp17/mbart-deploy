import time

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

base_url = "http://localhost:5000"
wait_time = 5
service = Service(ChromeDriverManager().install())
input_output_mapping = {
    "input 1": "output 1",
    "input 2": "output 2"
}


def send_input(driver, input_output):
    driver.get(base_url)
    driver.set_window_size(1920, 1053)
    text_area = driver.find_element(By.CSS_SELECTOR, "textarea")
    output_area = driver.find_element(By.CSS_SELECTOR, ".relative")
    submit_button = driver.find_element(By.XPATH, "//button[contains(.,'Submit')]")
    clear_button = driver.find_element(By.XPATH, "//button[contains(.,'Clear')]")
    for key, value in input_output:
        text_area.send_keys(key)
        submit_button.click()
        time.sleep(wait_time)
        assert value.strip() in output_area.text
        clear_button.click()


def click_example(driver, no_of_examples):
    driver.get(base_url)
    driver.set_window_size(1920, 1053)
    submit_button = driver.find_element(By.XPATH, "//button[contains(.,'Submit')]").click()
    for i in range(no_of_examples):
        driver.find_element(By.CSS_SELECTOR, "tr:nth-child(" + str(i) + ") .input_textbox_example").click()
        submit_button.click()
        time.sleep(wait_time)


class TestInput:
    def test_input(self):
        print("BASE URL: ", base_url)
        driver = webdriver.Chrome(service=service)
        try:
            send_input(driver, input_output_mapping)
            click_example(driver, 2)
        finally:
            driver.quit()

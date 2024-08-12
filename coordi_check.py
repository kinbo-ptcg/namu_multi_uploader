import pyautogui
import time

import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == '__main__':
    # Chrome for testing 위치 설정
    options = Options()
    options.binary_location = 'your CFT location'

    # ChromeDriverManager를 사용하여 ChromeDriver 설치 및 경로 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # 나무위키 이미지 업로드 페이지로 이동
    driver.get("https://namu.wiki/Upload")
    
    select_button = driver.find_element(By.XPATH, "//button[text()='Select']")
    select_button.click()  
    
    print('start')
    while True:
        x, y = pyautogui.position()
        print(f"X: {x} Y: {y}")
        time.sleep(1.0)
# 나무위키에 이미지 하나하나 업로드 하는게 너무 힘들다
# 그걸 Selenium.ChromeDriver, pyautogui를 이용해서 자동화 해본다.
# 이미지업로드에 필요한 정보는
# 1. 이미지 파일명
# 2. 나무위키에 업로드될 이미지의 이름
# 3. 출처 url
# 4. 라이선스종류(대부분 제한적 이용)
# 5. 분류

import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import pyperclip

def make_upload_detail(source):
    text_base = '''
[목차]
== 기본 정보 ==
|| 출처 || {source} ||
|| 날짜 || 이미지가 만들어진 날짜를 삽입해 주세요. ||
|| 저작자 || 이미지의 저작자를 삽입해 주세요. ||
|| 저작권 || 이미지의 저작권과 관련된 기타 정보를 삽입해 주세요. ||
|| 기타 || 기타 정보가 있으면 삽입해 주세요. ||

== 이미지 설명 ==
이미지의 자세한 설명을 적어 주세요.
'''
    return text_base.format(source=source)

def login_namu(namu_id, namu_pw):     
    # 나무위키 로그인창 열기
    driver.get("https://namu.wiki/member/login")
    sleep(3)
        
    # 사용자 ID 입력
    username_input = driver.find_element(By.NAME, "email")
    username_input.clear()
    username_input.send_keys(ID)

    # 비밀번호 입력
    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys(PW)
        
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]")
    login_button.click()
        
    # 캡챠 처리 대기 (수동)
    # 나무위키 로그인은 캡챠가 요구됨
    print("캡챠를 해결하고, 완료되면 터미널에서 'enter' 키를 누르세요.")
    input("")

    # 캡챠 처리 후 다음 단계로 진행
    print("캡챠가 해결되었습니다. 다음 작업을 시작합니다.")

ID = 'yourID'
PW = 'yourPW'
UPLOAD_DATA = 'pathOfYourJson'

if __name__ == '__main__':
    
    # Chrome for testing 위치 설정
    options = Options()
    options.binary_location = 'your CFT location'

    # ChromeDriverManager를 사용하여 ChromeDriver 설치 및 경로 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        login_namu(ID,PW)
        
        # JSON 파일 로드
        with open(UPLOAD_DATA, 'r') as f:
            images_info = json.load(f)
            
        # 나무위키 이미지 업로드 페이지로 이동
        driver.get("https://namu.wiki/Upload")
        
        for image_info in images_info:
            # 파일 선택 버튼 클릭
            select_button = driver.find_element(By.XPATH, "//button[text()='Select']")
            select_button.click()
            sleep(1)  # 파일 선택 창이 열리는 시간을 고려한 짧은 대기

            # PyAutoGUI를 이용하여 Finder에서 파일 선택
            # 단말마다 좌표가 다르니 적절히 찾을것
            # coordi_check.py 이용하면 현재 마우스 커서의 위치를 알수 있음
            # 이하는 작성자의 단말에서의 값
            # 폴더 쇼트컷   : 294 489
            # 검색창 클릭   : 920 257
            # 검색 폴더 선택 : 501 302
            # 첫결과 선택   : 430 364
            # 열기버튼      : 959 645
            print('click shortcut')
            pyautogui.moveTo(x=294, y=489)
            pyautogui.click()
            sleep(0.5)
            
            print('search')
            pyautogui.moveTo(x=920, y=257)
            pyautogui.click()
            pyperclip.copy(image_info['file_name'].split('.')[0].replace('&',' ').replace('「',' ').replace( '」',' '))
            pyautogui.hotkey('command','v')
            sleep(1)
            
            print('click folder')
            pyautogui.moveTo(x=501, y=302)
            pyautogui.click()
            sleep(3)
            
            print('click file')
            pyautogui.moveTo(x=430, y=364)
            pyautogui.click()
            sleep(0.5)
            
            print('click upload')
            pyautogui.moveTo(x=959, y=645)
            pyautogui.click()
            sleep(0.5)
            
            print('done')
            sleep(1)
            
            # 업로드명 입력
            upload_name_input = driver.find_element(By.NAME, "document")
            upload_name_input.clear()
            upload_name_input.send_keys(image_info['namu_img_name'])

            # 출처 입력
            source_input = driver.find_element(By.NAME, "text")
            source_input.clear()
            source_input.send_keys(make_upload_detail(image_info['source']))

            # 라이선스 입력
            dropdown_menu = driver.find_elements(By.CLASS_NAME,"vs__dropdown-toggle")[0]
            dropdown_menu.click()
            license_input = driver.find_element(By.ID,"licenseSelect")
            license_input.click()
            license_input.send_keys(image_info['license'])
            license_input.send_keys(Keys.RETURN)
            
            # 분류 입력
            category_input = driver.find_element(By.ID, "categorySelect")
            category_input.click()
            category_input.send_keys(image_info['category'])
            category_input.send_keys(Keys.RETURN)

            # 업로드 버튼 클릭
            upload_button = driver.find_element(By.XPATH, "//button[contains(text(), '업로드')]")
            upload_button.click()

            # 업로드 완료 후 대기 (페이지가 전환될 때까지)
            sleep(1)  # 필요에 따라 대기 시간을 조정하세요.

            # 새로운 이미지 업로드를 위해 다시 업로드 페이지로 이동
            driver.get("https://namu.wiki/Upload")

    finally:
        # WebDriver 종료
        driver.quit()


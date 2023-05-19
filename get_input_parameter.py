from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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

    # for id in ids:
    #     # print(id)
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

    # for id in ids:
    #     # print(id)
    return id
url = "http://210.110.39.89/adminlogin.php"
extract_input_ids(url)
extract_submit_ids(url)

driver = webdriver.Chrome(executable_path='chromedriver')

for id in extract_input_ids(url):
    s="#{0}".format(id)
    print(s)
    keys = ['pw', 'password', 'pwd']
    if any(key in s for key in keys):
        print(s)
    input_param=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, s))
)


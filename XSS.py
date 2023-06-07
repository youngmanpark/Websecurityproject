from urllib import parse
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen(pageUrl)
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.findAll("a"):
        if 'href' in link.attrs:
            pages.add(link.attrs['href'])
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                pages.add(newPage)
                getLinks(newPage)
def dicxss(url):
    module_name = "XSS"
    contents = ""
    is_cve = "Safe"

    url = "http://" + url
    getLinks(url)
    lst = list(pages)
    dic = {}
    d = 0
    for i in lst:
        check = parse.urlparse(lst[int(d)])
        check.geturl()
        if check.query:
            dic.update(parse.parse_qs(check.query))
        d += 1


    fname = "payloads.txt"
    with open(fname) as f:
        content = f.readlines()
    payloads = [x.strip() for x in content]
    vuln = []
    for payload in payloads:
        for t in dic.keys():
            payload = payload
            xss_url = url + "?" + t + "=" + payload
            r = requests.get(xss_url)
            if payload.lower() in r.text.lower():
                if(payload not in vuln):
                    vuln.append(payload)
                else:
                    continue
    if vuln:
        tmp_contents = "\n".join(vuln)
        contents += str(tmp_contents)
        is_cve = "Risk"

    return (module_name, contents.strip(), is_cve)
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import httplib2
import socket
from time import sleep


def getHtmlContent(url):
    http = httplib2.Http(cache=None, timeout=10)
    try:
        response, content = http.request(url)
    except socket.timeout:
        print("Can not access %s" % url)
        return None

    content = content.decode('utf-8')
    soup = BeautifulSoup(content, "lxml")
    return soup


def getProxies(soup):
    proxyList = []
    proxies = soup.find_all('tr')[1:]
    # print(soup)
    for proxy in proxies:
        ip = proxy.find_all('td')[0].get_text()
        port = proxy.find_all('td')[1].get_text()
        ip_port = "%s:%s" % (ip, port)
        proxyList.append(ip_port)

    return proxyList


def getKuaiDaiLiProxies(pageNum):
    PROXIES = []
    urls = []
    urls.append("http://www.kuaidaili.com/free/")
    defaultUrl = "http://www.kuaidaili.com/free/inha/%d/"
    for i in range(2, pageNum+1):
        url = defaultUrl % i
        urls.append(url)

    for url in urls:
        print(url)
        soup = getHtmlContent(url)
        proxies = getProxies(soup)
        # print(proxies)
        PROXIES.extend(proxies)
        sleep(3)

    PROXIES = list(set(PROXIES))
    return PROXIES


# if __name__ == "__main__":
#     PROXIES = getKuaiDaiLiProxies(5)
#     print(PROXIES)
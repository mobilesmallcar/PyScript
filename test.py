import urllib
from bs4 import BeautifulSoup
import requests
import random
import time
from selenium import webdriver
import threading

def getHTMLText(url,proxies):
    try:
        r = requests.get(url,proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        return 0
    else:
        return r.text
def get_ip_list(url):
    print("获取ip:")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'}
    web_data = requests.get(url,headers)
    soup = BeautifulSoup(web_data.text, 'html')
    ips = soup.find_all('tr')
    print(ips)
    print("============================================")
    ip_list = []
    with open("./storage/IP.txt","a+") as f:
        for i in range(1, len(ips)):
            tds = ips[i].find_all('td')
            ip = tds[0].text + ':' + tds[1].text

            ip_list.append(ip)
            f.write(ip+"\n")
#检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    return ip_list
def scrapyUrl(ip_list):
    proxys = ["--proxy-server=http://221.178.232.130:8080",
              "--proxy-server=http://61.131.160.177:9006",
              "--proxy-server=http://122.194.209.187:61234",
              "--proxy-server=http://59.37.18.243:3128",
              "--proxy-server=http://218.64.69.79:8080",
              "--proxy-server=http://222.90.110.194:8080",
              "--proxy-server=http://114.249.230.208:8000",
              "--proxy-server=http://222.184.59.8:808",
              "--proxy-server=http://27.128.187.22:3128",
              "--proxy-server=http://113.109.249.32:808",
              ]
    for ip in ip_list:
        proxys.append("--proxy-server="+ip)
    option = webdriver()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--start-maximized')
    j = 1
    for proxy in proxys:
        try:  # try..except..保证遇到TimeoutException报错不中断
            option.add_argument(proxy)
            driver = webdriver.Chrome(chrome_options=option)
            # driver = webdriver.Chrome()
            driver.get("https://blog.csdn.net/qq_44603585/article/details/120849922?spm=1001.2014.3001.5501")  # 博客链接
            # driver.get("https://blog.csdn.net/qq_44603585/article/details/105216491?spm=1001.2014.3001.5501")  # 博客链接
            # driver.get("https://blog.csdn.net/qq_44603585/article/details/110182400?spm=1001.2014.3001.5501")  # 博客链接
            # driver.get("https://blog.csdn.net/qq_44603585/article/details/107326628?spm=1001.2014.3001.5501")  # 博客链接
            # driver.get("https://blog.csdn.net/qq_44603585/article/details/107304902?spm=1001.2014.3001.5501")  # 博客链接
            # driver.get("https://blog.csdn.net/qq_44603585/article/details/111061225?spm=1001.2014.3001.5501")  # 博客链接
            # driver.get("https://blog.csdn.net/qq_44603585/article/details/104312638?spm=1001.2014.3001.5501")  # 博客链接
            j += 1
            print('第%d次刷新' % j)
            time.sleep(2)
            driver.quit()
        except Exception as e:
            print(e)
if __name__ == '__main__':
    for i in range(1,20):
        url = 'https://www.kuaidaili.com/free/inha/'+str(i)+"/"
        time.sleep(1)
        ip_list = get_ip_list(url)
    print(ip_list)
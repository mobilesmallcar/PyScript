import urllib.request
from urllib import request, parse
import requests
import random
import threading
import time
from selenium import webdriver

from selenium.webdriver.chrome.options import Options


def getProxysDictFromFile(fileName):
    ip_list = []
    with open(fileName,"r+") as f:
        temp = f.readline();
        while(len(temp)>5):
            myDict = {}
            myDict["http"] = temp.strip();
            temp = f.readline();
            ip_list.append(myDict)
    return ip_list
def getProxysListFromFile(fileName):
    ip_list = []
    with open(fileName,"r+") as f:
        temp = f.readline();
        while(len(temp)>5):
            ip_list.append(temp.strip())
            temp = f.readline();
    return ip_list
def writeIp(fileName):
    # 发送get请求
    proxys = getProxysDictFromFile(fileName)
    for proxy in proxys:
        try:
            print(url,headers,proxy)
            response = requests.get(url=url, headers=headers, proxies=proxy)
            f = open('storage/validIP2.txt', 'a+')
            f.write(str(proxy) + '\n')
            f.close()
            # print(response.text)
            ## 获取返回页面保存到本地，便于查看
            # with open('ip.html','w',encoding='utf-8') as f:
            #    f.write(response.text)
        except:
            print(proxy, '无效ip！')
def click(fileName):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--start-maximized')
    # option.add_argument('window-size=1920x3000')
    j = 1
    proxys = getProxysListFromFile(fileName)
    for proxy in proxys:
        try:  # try..except..保证遇到TimeoutException报错不中断
            print("=======")
            proxy = eval(proxy)["http"]
            print("--proxy-server=http://"+proxy)
            # print(type(proxy["http"]))
            # print(proxy.get("http"))
            option.add_argument("--proxy-server=http://"+proxy)
            driver = webdriver.Chrome(chrome_options=option)
            # driver = webdriver.Chrome()
            driver.get("https://blog.csdn.net/qq_44603585/article/details/105216491?spm=1001.2014.3001.5501")  # 博客链接
            j += 1
            print('第%d次刷新' % j)
            time.sleep(2)
            driver.quit()
        except Exception as e:
            with open("storage/error.txt","a+") as f:
                f.write(str(e))
                f.write("=============")
            print("错误了")
if __name__ == '__main__':
    # 用百度检测ip代理是否成功
    url = 'https://www.baidu.com/'
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    time.sleep(1)
    # writeIp("./storage/IP.txt")
    click("./storage/validIP2.txt")


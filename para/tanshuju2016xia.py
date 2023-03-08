import time
import random
from selenium import webdriver
from urllib.parse import unquote, quote

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import Keys

from selenium.webdriver.common.by import By


def login(driver, usr, pwd):
    passButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[1]/div[2]/div[1]/div[2]")

    passButton.click()

    time.sleep(0.5)
    name = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div[4]/div[1]/div[2]/div[2]/form[1]/div[1]/div/div/input")
    name.send_keys(usr)
    password = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[4]/div[1]/div[2]/div[2]/form[1]/div[2]/div/div/input')
    password.send_keys(pwd)
    # time.sleep(2)
    serviceTitle = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[4]/div[1]/div[2]/div[2]/form[1]/div[4]/label/span[1]/span')
    serviceTitle.click()
    button = driver.find_element_by_xpath('/html/body/div[1]/div/div[4]/div[1]/div[2]/div[2]/form[1]/button')
    button.click()


def findEnter(driver, branches):
    time.sleep(2)
    div = 1
    wantEnterName = branches[0]
    print(wantEnterName)
    enterName = ''
    while (enterName != wantEnterName):
        enterStr = "/html/body/div[1]/div/div[4]/main/div/div/div/div[2]/div[2]/div[2]/div[" + str(div) + "]"
        enterNameStr = enterStr + "/p"
        enter = driver.find_element_by_xpath(enterStr)
        enterp = driver.find_element_by_xpath(enterNameStr)
        enterName = enterp.text
        print(enterName)
        div = div + 1
    time.sleep(2)
    enter.click()
    time.sleep(2)
    driver.current_url
    driver.refresh()
    time.sleep(2)

def createCarbon(driver,timeList):
    timeEndYear = '2016'
    timeEndMouth = 12
    needbackYear = '2016'
    currentMounth = 7
    while(not(timeEndYear==needbackYear and timeEndMouth == currentMounth)):
        createButton = driver.find_element_by_xpath('/html/body/div/div/div[5]/div[2]/main/div/div/div/div[2]/div[1]/button[1]')
        createButton.click()
        time.sleep(0.2)
        back = driver.find_element_by_css_selector('#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text > div.d-flex.justify-space-between.align-center > button:nth-child(1)')

        checkBackYear = driver.find_element_by_css_selector('#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text > div.d-flex.justify-space-between.align-center > span').text
        while(needbackYear!=checkBackYear):
            back.click()
            checkBackYear = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div[1]/span').text
            time.sleep(0.1)

        while(currentMounth<=12):
            createFlag = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div[2]/div/div['+str(currentMounth)+']/div/div[2]').text
            if(createFlag=='待创建'):
                clickMouth(driver,currentMounth)
                time.sleep(4)
                cancel = driver.find_element_by_xpath('/html/body/div/div/div[5]/div[2]/main/div/div/div/div[2]/div/div/button[1]/span')
                cancel.click()
                currentMounth = currentMounth + 1
                break
            elif(createFlag=='待填报'):
                clickMouth(driver, currentMounth)
                time.sleep(2)
                # group = driver.find_element_by_class_name('v-slide-group__content')
                # groups = group.find_elements('div>span')
                driver.current_url
                driver.refresh()
                time.sleep(1)
                totalValue = driver.find_element_by_xpath('/html/body/div/div/div[5]/div[2]/main/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/input')
                if(totalValue.get_attribute('value') is None or totalValue.get_attribute('value')==''):
                    totalValue.send_keys(random.randint(7500,15000))
                groups_elements = driver.find_element_by_xpath('/html/body/div/div/div[5]/div[2]/main/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]')
                groups = groups_elements.find_elements_by_xpath('.//span')
                checkHasComplete = checkComplete(driver,groups)
                if checkHasComplete:
                    with open('result.txt', 'a+',encoding='utf-8') as f:
                        f.writelines(needbackYear + "年" + str(currentMounth) + "月\n")
                if not checkHasComplete:
                    for group in groups:
                        group.click()
                        time.sleep(3.3)
                        processes_elements = driver.find_element_by_xpath('/html/body/div/div/div[5]/div[2]/main/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[1]')
                        processes = processes_elements.find_elements_by_class_name('v-expansion-panel')
                        for process in processes:
                            button = process.find_element_by_xpath('.//button')
                            isPand = process.get_attribute('aria-expanded')
                            if(isPand=='false'):
                                button.click()
                            inputs = process.find_elements_by_xpath(".//input")
                            for input in inputs:
                                canRead = input.get_attribute("readonly")
                                if canRead is None:
                                    value = input.get_attribute('value')
                                    if value == '0.0':
                                        try:
                                            input.click()
                                            input.send_keys(random.randint(5, 20))
                                            totalValue.click()
                                        except:
                                            dz = driver.execute_script("arguments[0].scrollIntoView();", input)
                                        finally:
                                            input.click()
                                            input.send_keys(random.randint(5, 20))
                                            totalValue.click()
                confirm = driver.find_element_by_xpath('/html/body/div/div/div[5]/div[2]/main/div/div/div/div[2]/div/div/button[2]')
                confirm.click()
                currentMounth = currentMounth + 1
                break
            else:
                currentMounth = currentMounth + 1
            if(currentMounth==13):
                needbackYear = str(int(needbackYear) + 1)
                currentMounth = 1
                break
        driver.current_url
        driver.refresh()
        time.sleep(2)

def checkComplete(driver,groups):
    checkHasComplete = False
    checckGroup = groups[-1]
    checckGroup.click()
    processes_elements = driver.find_element_by_xpath(
        '/html/body/div/div/div[5]/div[2]/main/div/div/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[1]')
    time.sleep(1)
    time.sleep(1)
    processes = processes_elements.find_elements_by_class_name('v-expansion-panel')
    process = processes[-1]
    button = process.find_element_by_xpath('.//button')
    isPand = process.get_attribute('aria-expanded')
    if (isPand == 'false'):
        button.click()
    inputs = process.find_elements_by_xpath(".//input")
    for input in inputs:
        canRead = input.get_attribute("readonly")
        if canRead is None:
            value = input.get_attribute('value')
            if value != '0.0':
                checkHasComplete = True
    return checkHasComplete
def clickMouth(driver,currentMounth):
    mouth = driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div[2]/div/div[' + str(currentMounth) + ']/div')
    mouth.click()
    confirm = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[3]/button[2]/span')
    confirm.click()

def buildProjects():
    projects = []
    projects.append('积木碳云')
    # projects.append('积木碳云后台')
    return projects

def getTimeList():
    timeList = []
    timeList = '2015-01--2015-02'


if __name__ == '__main__':
    url = "http://122.144.182.9:1580/workbench/login"
    driver = webdriver.Chrome()
    driver.get(url)
    usr = "15190885141"
    pwd = "123456"
    login(driver, usr, pwd)
    # try:
    projects = buildProjects()
    findEnter(driver, projects)
    timeList = getTimeList()
    createCarbon(driver,timeList)
    # except:
    #     driver.close()


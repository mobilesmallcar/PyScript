import os
import re
import uuid

# def file_name(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         print(root)  # 当前目录路径
#         print(dirs)  # 当前路径下所有子目录
#         print(type(files))  # 当前路径下所有非目录子文件
#         for file in files:
def return_new_line(lines, temp):
    global i;
    i = temp + 1;
    line = lines[i];
    return line;

def find_des_by_mapping(lines,i):
    temp = i - 1
    line = lines[temp]
    while(("String" not in line )and temp > 5 ):
        temp = temp - 1;
        line = lines[temp]
        if("/**" in line ):
            urlName = re.findall(r'.*?/*\s{0,5}([\w|-]+)[\n]', lines[temp+1])[0]
            if (urlName == ''):
                urlName = re.findall(r'.*?/*\s{0,5}([\w|-]+)\s', lines[temp+1])[0]
            return find_url_by_mapping(lines[i],urlName)
    return False
def find_des_by_remark(lines,i):
    temp = i
    line = lines[temp]
    while("return" not in line):
        temp = temp -1
        line = lines[temp]
        if("scription" in line):
            print(line)
            urlName = re.findall(r"scription[:]?\s?([\w|-]+)[\n]",line)[0]
            if(urlName==''):
                urlName = re.findall(r"scription[:]?\s?([\w|-]+)[\n]\s",line)[0]
            return find_url_by_mapping(lines[i],urlName)
        elif("/**" in line):
            line = lines[temp+1]
            print(line)
            urlName = re.findall(r'.*?/*\s{0,5}([\w|-]+)[\n]',line)[0]
            if(urlName==''):
                urlName = re.findall(r'.*?/*\s{0,5}([\w|-]+)\s',line)[0]
            return find_url_by_mapping(lines[i],urlName)
    return False
def find_url_by_mapping(line, urlName):
    global urlDict,basicUrlName,basicFlag
    if ("Mapping(" in line):
        if ("UrlMapping" in line):
            url = re.findall(r'@.*?UrlMapping.(.*?)[\)|\s]', line)[0]
            print(url)
            # todo查找到对应urlMapping关系.
        else:
            url = re.findall(r'.*?@\w{3,4}Mapping.*?"(.*?)"', line)[0]
            print(url)
        if(basicFlag==True):
            if(basicUrlName[-1:]!="/"):
                url = basicUrlName+url
            else:
                url = basicUrlName[:-1]+url
        urlDict[url] = urlName
        return url
    return False;


def walk_dir(path, fileName):
    filter_file_name = fileName
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == filter_file_name:
                if "target" not in root:
                    value_dir = os.path.join(root, filter_file_name)
                    return value_dir


def match_url_by_url_mapping(absUrlPath, urlDict):
    with open(absUrlPath, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        global i,newUrlDict,urlMapping,paramMapping
        i = 1
        while (i < len(lines) - 1):
            line = return_new_line(lines, i)
            if ("String" in line):
                temp = re.findall(r'String\s{1,5}(\w{5,50})\s{0,5}', line)[0]
                if (urlDict.__contains__(temp)):
                    trueUrl = re.findall(r'=\s{0,5}"(.*?)"', line)[0]
                    uid = str(uuid.uuid4())
                    suid = ''.join(uid.split('-'))
                    paramMapping[suid] = {"reflect_model":"","reflect_url":trueUrl,"reflect_name":urlDict[temp],"reflect_mapping":temp}
                    newUrlDict[trueUrl] = urlDict[temp]
                    urlMapping[temp] = trueUrl


def find_controller(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if "Controller" in file:
                if "target" not in root:
                    absFile = os.path.join(root, file)
                    print(absFile)
                    find_url_and_name(absFile)
    return True

def change_url_slash():
    global newUrlDict
    for key in newUrlDict:
        if key[0:1] != "/":
            newUrlDict['/' + key] = newUrlDict[key]
            newUrlDict.pop(key)

def find_url_and_name(fileName):
    with open(fileName, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        global i,basicUrlName,basicFlag
        i = 1
        basicFlag = False
        basicUrlName = ""
        while (i < len(lines) - 2):
            flag = False
            line = return_new_line(lines, i)
            if ("@RequestMapping" in line):
                if ("method" in line):
                    5
                else:
                    basicUrlName = re.findall(r'@RequestMapping.*?"(.*?)"', line)[0]
                    flag = True
                    basicFlag = True
                    print("basicUrlName:" + basicUrlName)

            # if("Controller" in line):
            # 如果这个url没有信息则不会出现在dict里面
            # if("@ApiOperation" in line):
            #     urlName = re.findall(r'.*?@ApiOperation.*?"(.*?)"',line)[0]
            #     line = lines[i-1]
            #     status = find_url_by_mapping(line,urlName)
            #     if(status==False):
            #         line = lines[i+1]
            #         find_url_by_mapping(line,urlName)
            if(flag != True):
                if ("Mapping(" in line):
                    line = lines[i - 1]
                    if ("@ApiOperation" in line):
                        urlName = re.findall(r'.*?@ApiOperation.*?"(.*?)"', line)[0]
                        find_url_by_mapping(lines[i], urlName)
                    else:
                        line = lines[i + 1];
                        if ("@ApiOperation" in line):
                            urlName = re.findall(r'.*?@ApiOperation.*?"(.*?)"', line)[0]
                            find_url_by_mapping(lines[i], urlName)
                        else:
                            #url没有备注信息
                            urlName = "暂无url信息"
                            #查controller备注信息
                            status = find_des_by_remark(lines,i)
                            if(False == status):
                                status = find_des_by_mapping(lines,i)
                                if(False == status):
                                    find_url_by_mapping(lines[i], urlName)


if __name__ == '__main__':
    # global i;
    # dir = r"F:\test"
    dir = r"D:\guomao\itg-basic"
    # Search(dir,'txt','a')
    # file_name(dir)
    urlDict = dict()
    newUrlDict = dict()
    urlMapping = dict()
    paramMapping = dict()
    find_controller(dir)
    absUrlPath = walk_dir(dir, 'UrlMapping.java')
    match_url_by_url_mapping(absUrlPath, urlDict)
    change_url_slash()
    print(len(urlDict))
    print(urlDict)
    print(newUrlDict)
    print(urlMapping)
    print(paramMapping)

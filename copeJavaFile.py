import os
import re
import uuid
import requests


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


# mapping文件的url名称补偿
def find_des_by_mapping(lines, var, i):
    temp = i - 1
    line = lines[temp]
    while (("String" not in line) and temp > 5 and ("private" not in line)):
        temp = temp - 1;
        line = lines[temp]
        if ("scription" in line):
            urlName = re.findall(r"scription[:]?\s+([\w|-]+)\s*.*?[\n]", line)[0]
            urlDict[var] = urlName
            return True
        elif ("/**" in line):
            urlName = re.findall(r'\s+/*\s{0,5}([\w|-]+).*?[\n]', lines[temp + 1])[0]
            urlDict[var] = urlName
            return True
    return False


def find_des_by_remark(lines, i):
    temp = i
    line = lines[temp]
    while ((" return" not in line) and ("private" not in line)):
        temp = temp - 1
        line = lines[temp]
        if ("scription" in line):
            urlName = re.findall(r"scription[:]?\s+([\w|-]+)\s*.*?[\n]", line)[0]
            return find_url_by_mapping(lines[i], urlName)
        elif ("/**" in line):
            line = lines[temp + 1]

            try:
                if ("（" in line or "(" in line):
                    urlName = re.findall(r'[(|（]([\w|-]+)[)|）]', line)[0]
                else:
                    urlName = re.findall(r'.*?/*\s*([\w|-|,|\s]+)[\n]', line)[0]
            except:
                print("异常:===", line, "===")
                return False;
            return find_url_by_mapping(lines[i], urlName)
    return False


def find_url_by_mapping(line, urlName):
    global urlDict, basicUrlName, basicFlag
    if ("Mapping(" in line):
        if ("UrlMapping" in line):
            url = re.findall(r'@.*?UrlMapping.(.*?)[\)|\s|,]', line)[0]
            print("urlMapping", url)
            # todo查找到对应urlMapping关系.
        else:
            url = re.findall(r'.*?@\w{3,7}Mapping.*?"(.*?)"', line)[0]
            print("url", url)
        if (basicFlag == True):
            if (basicUrlName[-1:] != "/"):
                url = basicUrlName + url
            else:
                url = basicUrlName[:-1] + url
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


def match_url_by_url_mapping(absUrlPath,isMapping):
    if(isMapping):
        with open(absUrlPath, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            global i, urlDict, newUrlDict, urlMapping, paramMapping
            i = 1
            while (i < len(lines) - 1):
                line = return_new_line(lines, i)
                if ("String" in line):
                    temp = re.findall(r'String\s{1,5}(\w{5,50})\s{0,5}', line)[0]
                    if (urlDict.__contains__(temp)):
                        if (urlDict[temp] == None):
                            find_des_by_mapping(lines, temp, i)
                        trueUrl = re.findall(r'=\s{0,5}"(.*?)"', line)[0]

                        build_dict(trueUrl,urlDict[temp],temp)
                        urlDict.pop(temp)
                        # newUrlDict[trueUrl] = urlDict[temp]
                        # urlMapping[temp] = trueUrl
    #补偿对于mapping里面不存在的url
    for key,value in urlDict.items():
        build_dict(key,value,None)
    urlDict = {}
    change_url_slash()
def build_dict(key,value,mapping):
    uuid = new_uuid()
    paramMapping[uuid] = {"reflectModel": tempServer, "reflectUrl": key,
                          "reflectName": value, "reflectMapping": mapping}

def new_uuid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid
def find_controller(path):
    global server
    global tempServer
    server = ""
    tempServer = "basic"
    for root, dirs, files in os.walk(path):
        for file in files:
            if "Controller" in file:
                if "target" not in root:
                    if ("com\\ry") in root:
                        server = re.findall(r'com\\ry\\\w+\\(.*?)\\', root)[0]
                        absFile = os.path.join(root, file)
                        print("path:" + absFile, "server:" + server)
                        find_url_and_name(absFile)
            if tempServer != server and server != "":
                printDict()
                tempServer = server
    return True
def printDict():
    global tempServer,server
    if("itg" in dir):
        mapping_dir = dir[:20]
    else:
        mapping_dir = dir + "\itg-" + tempServer
    print("mappingdir", mapping_dir)
    absUrlPath = walk_dir(mapping_dir, 'UrlMapping.java')
    print("mappingdir",absUrlPath)
    #对于没有urlmapping文件的情况
    flag = True
    if(absUrlPath==None):
        flag = False
    match_url_by_url_mapping(absUrlPath,flag)
    print(len(urlDict))
    print("urlDict",urlDict)
    print(len(newUrlDict))
    print("newUrlDict",newUrlDict)
    print(len(urlMapping))
    print("urlMapping",urlMapping)
    print(len(paramMapping))
    print("paramMapping",paramMapping)


def change_url_slash():
    for key,value in paramMapping.items():
        url = value["reflectUrl"]
        if url[0:1] != "/":
            value["reflectUrl"] = "/"+url


def find_url_and_name(fileName):
    with open(fileName, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        global i, basicUrlName, basicFlag
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
                    try:
                        basicUrlName = re.findall(r'@RequestMapping.*?"(.*?)"', line)[0]
                    except:
                        print("异常line" + line)
                        continue
                    flag = True
                    basicFlag = True
                    print("basicUrlName:" + basicUrlName)

            if (flag != True):
                if ("Mapping(" in line and "//" not in line):
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
                            # url没有备注信息
                            urlName = None
                            # 查controller备注信息
                            status = find_des_by_remark(lines, i)
                            if (False == status):
                                find_url_by_mapping(lines[i], urlName)

                            #     status = find_des_by_mapping(lines,i)
                            #     if(False == status):
                            #         print(lines[i])
                            #         find_url_by_mapping(lines[i], urlName)

def call_interface_insert_url_info():
    for key,value in paramMapping.items():
        print(value)
        r = requests.post("http://localhost:8003/n/reflectInterface/insertUrlInfo",json=value)
        print(r.text)
if __name__ == '__main__':
    # global i;
    # dir = r"F:\test"
    dir = r"D:\guomao"
    # Search(dir,'txt','a')
    # file_name(dir)
    urlDict = dict()
    newUrlDict = dict()
    urlMapping = dict()
    paramMapping = dict()
    find_controller(dir)
    printDict()
    call_interface_insert_url_info()
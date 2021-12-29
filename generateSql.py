import re
import requests
from requests_toolbelt import MultipartEncoder
from time import ctime,sleep
# import requests_toolbelt
import copy
# 物料7个0 size>15  INTO `(.*?)` VALUES.*?\'([0]{7}\d{8}.*?)\'
# 供应商\客商 size=10 00开头  INTO `(.*?)` VALUES.*?\'([0]{2}\d{8}.*?)\'
# 合同 size=10 00开头
# 采购订单size=10 4开头   INTO `(.*?)` VALUES.*?\'([4]{1}[4-5]{1}\d{8}.*?)\'
# 合同类型Z开头 4位        INTO `(.*?)` VALUES.*?\'([Z]{1}\d{3}.*?)\'
def print_hi(table,myList):
    with open("dataBase/"+table+".txt", "r+", encoding="utf-8") as f:
        lines = f.readlines();
        i=0
        needList = []
        tempList = []
        httpList = []
        count = 0
        myMateDict = {}
        myPurchaseDict = {}
        myPayTypeDict = {}
        myIndefineDict = {}
        while(i < len(lines)-1):
            line = lines[i]
            tableName = re.findall(r'CREATE TABLE `(.*?)`.*?\(', line)
            if(len(tableName)):
                if(count==0):
                    count += 1
                else:
                    needList.append(tempList)
                    tempList = []
                tempList.insert(0, tableName)
            mate = re.findall(r'INTO `(.*?)` VALUES.*?\'([0]{7}\d{8}.*?)\'',line)
            if(len(mate)>0):
                myMateDict[mate[0][0]] = mate[0][1]
            purchase = re.findall(r'INTO `(.*?)` VALUES.*?\'([4]{1}[4-6]{1}[0]{2}\d{6}.*?)\'',line)
            if (len(purchase) > 0):
                myPurchaseDict[purchase[0][0]] = purchase[0][1]
            payType = re.findall(r'INTO `(.*?)` VALUES.*?\'([Z]{1}\d{3}.*?)\'',line)
            if (len(payType) > 0):
                myPayTypeDict[payType[0][0]] = payType[0][1]
            indefineDict = re.findall(r'INTO `(.*?)` VALUES.*?\'([0]{2}\d{8})\'',line)
            if (len(indefineDict) > 0):
                myIndefineDict[indefineDict[0][0]] = indefineDict[0][1]
            name = re.findall(r'.*`(.*?)[`].*\'(.*?)\'',line,re.M)
            if(len(name)>0):
                # print(name)
                field = name[0][0]
                if(field in myList):
                    tempList.append(name[0])
            i = i + 1

        needList.append(tempList)
        print("根据长相匹配")
        print(myMateDict)
        print("物料:"+str(len(myMateDict)))
        print(myPurchaseDict)
        print("采购订单:"+str(len(myPurchaseDict)))
        print(myPayTypeDict)
        print("方式:"+str(len(myPayTypeDict)))
        print(myIndefineDict)
        print("供应商\客商||合同:"+str(len(myIndefineDict)))
        # print("长相匹配应该生成"+str(len(myMateDict)+len(myPurchaseDict)
        #       +len(myPayTypeDict)+len(myIndefineDict)+"个txt"))
        print("======================")
        return needList
def send_url(field,url,endName):
    # fileTop = "C:\\Users\\31209\\Desktop\\11月工作相关\\对照表\\"
    fileTop = "C:\\Users\\31209\\Desktop\\test\\"
    #物料
    if("mate"==field or "mblnr"==field
            or "commodity_code"==field or "product_code"==field):
        url += "&name=(物料)" + endName + ".txt"
        fileName = fileTop+"UAT新旧物料对照.xlsx"
    #采购订单
    elif("sap_ebeln"==field or "ebeln"==field or
         "transfer_sap_ebeln"==field or "procure_order_code"==field
         or "purchase_code"==field or "potype"==field):
        url += "&name=(采购订单号)" + endName + ".txt"
        fileName = fileTop + "UAT 采购订单对照表.xlsx"
    #todo or "SAP_CODE"==field 生成member的时候
    elif ("member_sap_code" == field):
        url += "&name=(客商代码)" + endName + ".txt"
        fileName = fileTop + "UAT 客商对照表.xlsx"
    elif ("supplier_code" == field or "SAP_CODE"==field or "item_code"==field):
        url += "&name=(供应商)" + endName + ".txt"
        fileName = fileTop + "UAT 客商对照表.xlsx"
    elif ("sap_tkonn" == field or "sap_contract_code"==field or "budget_sap_contract_code"==field):
        url += "&name=(合同号)" + endName + ".txt"
        fileName = fileTop + "UAT 合同对照表.xlsx"
    elif ("pay_type"==field or "contract_type" == field or "payment_method" == field ):
        url += "&name=(合同类型)" + endName + ".txt"
        fileName = fileTop + "UAT 部分栏位对照表.xlsx"
    else:
        return 0
    param = {
        'type': '13',
        'interval_id': '100:90',
        'action': '',
        'start': '20',
    }
    m = MultipartEncoder(
        fields={
            'file': (fileName, open(fileName, 'rb+'), "type=application/wps-office.xlsx")
        }
    )
    print(url)
    headers = {'Content-Type': m.content_type, 'accept': 'application/json'}
    response = requests.post(url, headers=headers, data=m, timeout=30)
    # state_test = eval(response.text)
    # print(state_test)
def getPatternStr():
    with open("pat/pattern.txt", "r+", encoding="utf-8") as f:
        s = f.readline().strip("\n")
        myList = []
        while(len(s)>0):
            myList.append(s)
            s = f.readline().strip("\n")
        return myList

if __name__ == '__main__':
    table = "basic"
    # url = "http://localhost:80/uploadexcel?"
    # str = "type=t_ware_reissue_return&field=pay_type&name=(合同类型)移库单子表.txt"
    # pattern = re.compile(r'\d+')
    # m = pattern.match('one12twothree34four', 3, 10)
    myList = getPatternStr()
    print(myList)
    print("======================")
    count = 0
    needList = print_hi(table,myList)
    for temp in range(len(needList)):
        count += len(needList[temp])-1
        print(needList[temp])
    print("总共会生成:"+str(count)+"个txt")
    for temp in range(len(needList)):
        myTuple = needList[temp]

        if(len(myTuple)>1):
            for field in range(1,len(myTuple)):
                url = "http://localhost:80/getUpdateSqlByBatch?"+\
                      "tableName="+table+"&type="+myTuple[0][0]+"&field="+myTuple[field][0]
                uploadLocation = "C:\\Users\\31209\\Desktop\\"+myTuple[0][0]+".txt"
                # sleep(1)
                # print(url+"&"+myTuple[0][0]+".txt")
                send_url(myTuple[field][0], url,myTuple[0][0])
    sleep(7)


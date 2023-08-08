import http.client
import json
import xmltodict
import base64
import time
import ssl
import socket

socket.setdefaulttimeout(90)
ssl._create_default_https_context = ssl._create_unverified_context

HOSTARM   = input("请输入ip地址:")
PORT      = int(input("请输入端口号:"))
USER_NAME = input("请输入用户名:")
PASSWORD  = input("请输入密码:")
BODY = input("请填写body信息:")

_RESTRICTED_SERVER_CIPHERS = "ALL"


DEFAULT_HEADER = {
                    "Connection"    : "Keep-Alive",
                    "Accept"       : "application/yang-data+xml",
                    "Content-Type"  : "application/yang-data+xml",
                 }

userPasswordStr = '%s:%s' % (USER_NAME, PASSWORD)

USERNAME_PASS = base64.b64encode(bytes(userPasswordStr.encode(encoding='utf-8'))).decode()

def fix_header():       #密码添加到头部
    headers = DEFAULT_HEADER.copy()
    headers['Authorization'] = 'Basic '  + USERNAME_PASS
    return headers

def send_request(method, url, body):
   #  context = ssl._create_default_https_context()     #security version tlsv1 tlsv1.1 tlsv1.2
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)      #sercurity version tlsv1.2
    context.set_ciphers(_RESTRICTED_SERVER_CIPHERS)
    httpClient = http.client.HTTPSConnection(HOSTARM, PORT, timeout=30, context=context)        #请求链接
    headers = fix_header()

    try:
        timestart = time.perf_counter()
        httpClient.request(method, url, body=body, headers=headers)         #发送请求
        print("request sent!")
        response = httpClient.getresponse()
        print("response received!")

        resp_status = response.status
        resp_headers = response.getheaders()
        timeend = time.perf_counter()
        timecost = timeend - timestart
        print("cost time: %0.6s s" % timecost)
        print("status: " + str(resp_status) + "\nResponse Headers: " + str(resp_headers[3]))

        resp_str = response.read()
        print("The Content-Length: " + str(len(resp_str)))
        # print(bytes.decode(resp_str,"utf8","ignore"))
        xmlparse = xmltodict.parse(resp_str)        #返回值转换json格式
        jsonstr = json.dumps(xmlparse,indent=1)
        print(jsonstr)
        httpClient.close()
    except Exception as e:
        print("Exception: %s" % e)
        print(e.args)
        httpClient.close()
    return 0

def test():
    METHODs = input('''
    1.PUT
    2.GET
    3.POST
    4.DELETE
    请输入使用的编号:''')
    while True:
        if METHODs == "1":
            METHODs = "PUT"
        elif METHODs == "2":
            METHODs = "GET"
        elif METHODs == "3":
            METHODs = "POST"
        elif METHODs == "4":
            METHODs = "DELETE"
        else:
            print("请输入正确的请求方法")
        break
    PATHS = input("请输入相关api:")
    send_request(METHODs, PATHS, BODY)
    return

if __name__ == '__main__':
    test()

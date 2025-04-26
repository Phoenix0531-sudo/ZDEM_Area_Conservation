#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#功能说明： 用户运行程序后自动检测认证状态：
#  1. register()生成DES+base64加密的注册码，保存到register.txt

import base64
#import pyDes
from pyDes import *

#设置注册信息
#ontent = self.getCombinNumber() 
end_version = '2.9'
user = 'try' #input('输入您的用户名，例如lichangsheng，请输入:')
valid_to = '2023-07-21' #input('输入软件有效日期，例如2021-04-22，请输入:')

class register:
    def __init__(self):
        self.Des_Key = "zdem2@bj" # Key
        self.Des_IV = "\x15\1\x2a\3\1\x23\2\0" # 自定IV向量

#DES+base64加密
    def Encrypted(self,tr):
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        EncryptStr = k.encrypt(tr)
        #EncryptStr = binascii.unhexlify(k.encrypt(str))
      ###  print('注册码：',base64.b64encode(EncryptStr))
        return base64.b64encode(EncryptStr) #转base64编码返回

#生成注册文件
    def regist(self):
        info= """%s
%s
end-version = %s
extra-data = %s
valid_to = %s""" % ('[ZDEM2JPG]','lic_ver = 200',end_version,user,valid_to)

        print('加密前:\n***\n%s\n***' %(info) )
        infobyte=bytes(info, encoding='utf-8')
        infobyteEncrypted=self.Encrypted(infobyte)
        
        print('*************')
        print('加密后:',infobyteEncrypted)
        print('*************')
###            print(type(content)) 

        print("gen succeed.") 
        #读写文件要加判断
        with open('./zdem.lic','a') as f:
            #f.buffer.write(infobyteEncrypted)
            infoEncrypted=infobyteEncrypted.decode('utf-8','ignore') # 忽略非法字符，用strict会抛出异常
            
#[ZDEM2JPG]
#lic_ver = 200
#end-version = 2.9
#extra-data = try
#valid-to = 2021-05-01
#sig = eD/75HrqgBBhGIqAnnC1mryikyojqeCdhWsqygZuSbf1llolEQ9mkIOGTHeseH9FZ/+q7I+PE8gD25n8++wtDJa9cbiZtFhY4Lirvg0YTM/fjek4d1CwhAMf1IXLXOUV++9iL5QAMwOVzO2D/0DiZuQf79aMZ1qNmYBF/1sDbv4=

            data = """%s
sig = %s

""" % (info,infoEncrypted)

            f.write(data)
            f.close()
        return True

reg=register()
reg.regist()


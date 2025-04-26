#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#功能说明： 用户运行程序后自动检测认证状态：
#  1. 解密注册文件中DES+base64加密的注册码
#  2. 判断软件有效期和用户名时候一致。如果一致则通过，不一致则让用户联系李长圣获取新的许可证

import base64
from pyDes import *
from datetime import datetime, timedelta
import time
import getpass
import os
import configparser
from pathlib import Path

class register:
    def __init__(self,version,VBOXscriptDir):
        self.version=version
        self.VBOXscriptDir=VBOXscriptDir
        #print("self.version",self.version)
        #print("self.VBOXscriptDir",self.VBOXscriptDir)
        self.Des_Key = "zdem2@bj" # Key
        self.Des_IV = "\x15\1\x2a\3\1\x23\2\0" # 自定IV向量


    def getUserName(self):
        # 获得用户名和当前时间
        username=getpass.getuser()
        #print("username",username)
        return username

 #des+base64解码
    def DesDecrypt(self,tr):
        tr = base64.b64decode(tr)
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        DecryptStr = k.decrypt(tr)
        #print('DecryptStr ：',DecryptStr )
        #return base64.b64decode(DecryptStr) #转base64解码返回
        return DecryptStr

# 打开程序先调用注册文件，比较注册文件中注册码与此时获取的硬件信息编码后是否一致
    def checkAuthored(self):
        contactsheng='请联系李长圣博士<sheng0619@163.com>，获取许可证。'
        #读写文件要加判断
        LicenseFile = self.VBOXscriptDir+'/zdem.lic'
        my_file = Path(LicenseFile)
        if (not my_file.exists()):
            #print("文件不存在，***colormapfile:",colormapfile)
            # 指定的文件存在	
            LicenseFile=os.path.join(os.environ['HOME'],'zdem.lic')
            if ( os.path.isfile(LicenseFile) == False ):
                print("\t找不到许可证文件,%s" %(contactsheng),flush=True)
                os._exit(0)
        #print("LicenseFile:", LicenseFile)

        try:
            #f=open(LicenseFile,'r')
            
            #读取
            cf=configparser.ConfigParser()
            cf.read(LicenseFile)
            #print(cf)  
            if cf:
                #读取zdem.lic中的明码字符信息
                items = cf.items("ZDEM2JPG")  # 获取键值对
                items = items[0:-1] #去除最后一个sig
                #print('明码:',items)
                # [('a_key1', '20'), ('a_key2', '10')]
                
                #解码zdem.lic中的加密后的sig字符信息
                sig=cf.get("ZDEM2JPG","sig")
#                print(type(sig))  #--><class 'str'>
#                print('sig<%s>' %(sig) )
                value_decrypted=bytes(sig, encoding='utf-8')   # 注册文件中注册码
                #print('value_decrypted:<%s>' %(value_decrypted) )
                ZDEM2JPGdecryptedByte=self.DesDecrypt(value_decrypted)
                #byte转字符串
                ZDEM2JPGdecrypted=ZDEM2JPGdecryptedByte.decode('utf-8','ignore') # 忽略非法字符，用strict会抛出异常
                #print('ZDEM2JPGdecrypted:\n***\n%s\n***' %(ZDEM2JPGdecrypted) )
                
                #读取zdem.lic中的解密后sig中的字符信息
                configDecrypted = configparser.ConfigParser()
                configDecrypted.read_string(ZDEM2JPGdecrypted)
                itemsDecrypted = configDecrypted.items("ZDEM2JPG")  # 获取键值对
                #print('解码:',itemsDecrypted)
                #自己检查解码后的sig与明码是否一致
                if (items != itemsDecrypted):
                    #print('items != itemsDecrypted',(items != itemsDecrypted))
                    print('\t许可证书失效！%s' %(contactsheng),flush=True)
                    os._exit(0)

                #opts=configDecrypted.options("ZDEM2JPG")  # 获取区域的所有key
#                print(opts)
                end_version=configDecrypted.get("ZDEM2JPG","end-version")
                extra_data=configDecrypted.get("ZDEM2JPG","extra-data")
                valid_to=configDecrypted.get("ZDEM2JPG","valid_to")
#                print(extra_data)
#                print(valid_to)
#                #os._exit(0)

                #时间判断
                YMDpresent= time.strftime("%Y-%m-%d", time.localtime())
                YMDindate=valid_to
                #print("日期YMDpresent", YMDpresent)
                #print("日期valid_to", valid_to)
                datetimeYMDpresent= datetime.strptime(YMDpresent, '%Y-%m-%d')
                datetimevalid_to= datetime.strptime(valid_to, '%Y-%m-%d')
                #print("日期", datetimeYMDpresent > datetimevalid_to)
                
                #用户名判断
                userName = self.getUserName()
                UserNameDesDecrypt=extra_data
                #print("userName", userName)
                #print("UserNameDesDecrypt", UserNameDesDecrypt)

                if (datetimeYMDpresent >= datetimevalid_to) :
                    print('\t许可证过期！%s' %(contactsheng),flush=True)
                    os._exit(0) #不抛出异常，退出

                if ((userName != UserNameDesDecrypt) and (UserNameDesDecrypt != 'try')):
                    print('\t许可证签名与当前许可证书不匹配！%s' %(contactsheng),flush=True)
                    os._exit(0)
                
                #print("self.version",self.version)
                #print("end_version",end_version)
                #print("( self.version >= end_version):",(self.version > end_version))
                if (self.version >= end_version) :
                    #print('当前软件版本%s'%(self.version) )
                    print('\t许可证书已失效！%s' %(contactsheng),flush=True)
                    os._exit(0)

                #print('通过认证。')
                
            else:
                print('\t许可证文件<%s>件中不能被打开！%s' %(LicenseFile,contactsheng),flush=True )
        except:
            print('\t许可证文件<%s>错误！%s' %(LicenseFile, contactsheng),flush=True )
            os._exit(0)

#reg=register('2.0','.')
#reg.regist()
#reg.checkAuthored()



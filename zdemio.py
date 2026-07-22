#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
#for pyinstall
from pathlib import Path
import numpy as np

def usage(softwareName):
	#print("------do not give the dir of data , usage:----------")
	print("用法: %s --dir=./data --dpi=300" %(softwareName) )
	print("	-------参数说明----------")
	print("	--dir   VBOX数据所在目录")
	print("	--xmax 绘图X最大值")
	print("	--ymax 绘图Y最大值")
	print("	--xmin 绘图X最小值，默认0.0")
	print("	--ymin 绘图Y最小值，默认0.0")
	print("	--xmove 坐标沿x轴偏移量，默认0.0")
	print("	--ymove 坐标沿y轴偏移量，默认0.0")
	print("	--major_locator 主坐标刻度间隔，默认10000")
	print("	--minor_locator 次坐标刻度间隔，默认1000")
	print("	--fontsize 坐标刻度字体大小，默认9")
	print("	--max_workers 并行进程数，默认24")
	print("	--dpi 图片分辨率，默认600")
	print("	--linewidth 线粗细，默认0.5")
	print("	--pagesize 图片大小，单位cm，默认14")	
	print("	--leftshow 显示坐标轴左线框，取值true/false，默认true")
	print("	--rightshow 显示坐标轴右边框，取值true/false，默认true")	
	print("	--bottomshow 显示坐标轴下线框，取值true/false，默认true")
	print("	--topshow 显示坐标轴上边框，取值true/false，默认true")
	print("	--wallshow 显示wall墙，取值true/false，默认true")
	print("	--surfaceshow 显示变形边界true/false，默认true")
	print("	--bondplot 绘制粘结连接关系true/false，默认false，黑色是没有粘结，红色是有粘结拉伸状态，蓝色是有粘结挤压状态")
	print("	--ballplot 绘制颗粒true/false，默认true")
	print("	--colormap 指定颜色配置文本文件，格式为10x3的矩阵，对应十个RGB值．")
	print("")
	print("	-v 打印版本号")
	print("	-h 打印此帮助信息")

def get_file_list(DataDir,FileNamePrefix,FileNameSuffix):
	"""获取指定目录下符合前后缀的文件列表。"""
	pathDir = os.listdir(DataDir)
	ListFile = [] #result
	for FileName in pathDir:
			#print ("s:%s"%(s))
			newDir=os.path.join(DataDir,FileName)
			#print ("newDir:%s"%(newDir))
			if os.path.isfile(newDir) :         #Èç¹ûÊÇÎÄ¼þ
				#print ("file:%s"%(newDir))
				#if os.path.splitext(newDir)[1]==FileType:  #ÅÐ¶ÏÊÇ·ñÊÇtxt
					#print ("txt:%s"%(newDir))
				#tempFileDir  = os.path.split(newDir)[0] #
				tempFileName = os.path.split(newDir)[1] #
				#print ("tempFileName:%s"%(tempFileName))
					#print (tempFileName.find('log')==-1)
				#print ("newDir:%s"%(newDir))
				#dont't save log file
				if (tempFileName.find(FileNamePrefix) != -1) and  (tempFileName.find(FileNameSuffix) != -1):
					#if tempFileDir.find('wu_zhenyun')==1:
					#print ("don't have 'log '%s"%(newDir))
					#backup_file(newDir,fixoldDir,backupDir)
					#print ("tempFileName:%s"%(tempFileName[0:2]))
					ListFile.append(newDir)
					#print ("newDir:%s"%(newDir))
	return ListFile

def read_data(filename):
	"""
	2019/01/07
	LI ChangSheng @ Nanjing University
	read zdem data

	input：
	[1] zdem data dir <./data>

	output：
	[1] wall, ball
	
	example:
	WALL,BALL,CONTACT,BOND,CurrentStep=read_data("./all_0000101000.dat")

	"""

	flag = 0
	#header = []
	WALL = []
	BALL = []
	CONTACT=[]
	BOND=[]
	GROUP = []
	vbcontact= 'False'
	vbbond='False'
	zdemfile = open(filename, "r")#, encoding = 'utf-8')

	for line in zdemfile:
		#if "ball data" in line:
		#	header.append(line)
		#	flag = 1
		#	continue
		#print(line,'flag',flag)
		if "     index         id      P1[0]" in line: #mark the beginning of wall data
			flag = 1
			continue
		if "     index         id         xF" in line: #quit as the wall data goes to end
			flag = 0
		if "     index         id                    x" in line: #mark the beginning of cell data
			flag = 2
			continue
		if "     index         id            m" in line: #quit as the cell data goes to end
			flag = 5
			continue
		if "contact data ..." in line: #record contact
			vbcontact='true'
			continue
		if "id1" in line and vbcontact=='true': #record contact
			flag =3
			continue
		if "bond data ..." in line: #record contact
			vbbond = 'true'
			flag=4
			vbcontact='false'
			#print('12')
			continue
		if "       id1" in line and vbbond == 'true' : #record contact
			flag =4
			continue
		if 'current_step' in line :
			step_info = line.split()
			CurrentStep=step_info[-1]
		if flag == 0:
			#header.append(line)
			continue
		if flag == 1:
			wall_info = line.split()
			WALL.append(wall_info)
		
		if flag == 2:
			#print line
			ball_info = line.split()
			#ball_info = [ float(i) for i in ball_info[2:6] ]
			BALL.append(ball_info)
		if flag == 3:
			#print ("3")
			contact_info = line.split()
			contact_info = [ int(i) for i in contact_info[0:2] ]
			CONTACT.append(contact_info)
		if flag == 4:
			#print line
			bond_info = line.split()
			bond_info = [ i for i in bond_info[0:3] ]
			BOND.append(bond_info)
		if flag == 5:
			temp = line.split()
			if len(temp) != 0:
				if len(temp) > 10 and 'contact' not in line and 'bond' not in line:
					GROUP.append([temp[1], temp[10]])
				else:
					flag = 0
					continue
			
	del WALL[-1] #del last NULL line
	del BALL[-1] #del last NULL line
	if CONTACT == []:
		CONTACT =[1]
	if BOND == []:
		BOND =[1]
	del CONTACT[-1] #del last NULL line
	del BOND[-1] #del last NULL line
	#print(CONTACT,BOND)
	zdemfile.close()
	#print(BOND)
	
	return  WALL, BALL, CONTACT, BOND, CurrentStep, GROUP

def BallListStrToNumpyArray(BALL):
	"""
	转换为numpy数据类型matrix
	输入参数：
	[1]BALL  颗粒信息nx6 [ index id x y r color]
	输出参数：
	[1]BALLid     nx1
	[2]BALLxyn2   nx2
	[4]BALLr      nx1
	[5]BALLcolor  nx1
	"""
	#list(map(int,BALL))
	IDList    = [int(oneInfo[1])   for oneInfo in BALL]
	UxList    = [float(oneInfo[2]) for oneInfo in BALL]
	UyList    = [float(oneInfo[3]) for oneInfo in BALL]
	RADList    = [float(oneInfo[4]) for oneInfo in BALL]
	COLORList = [int(oneInfo[5])   for oneInfo in BALL]
	
	BALLId=np.matrix(IDList).T
	BALLx=np.matrix(UxList).T
	BALLy=np.matrix(UyList).T
	BALLxyN2 = np.hstack((BALLx,BALLy))
	
	BALLRad=np.matrix(RADList).T
	BALLColor=np.matrix(COLORList).T
	return BALLId, BALLxyN2, BALLRad, BALLColor

def  WallListStrToNumpyArray(WALL):
	"""
	转换为numpy数据类型
	输入参数：
	[1]WALL  墙体信息nx6 [ index id P1x P1y P2x P2y ]
	输出参数：
	[1]WALLid           nx1 [id]
	[2]WALLP1P2xyxyN4   nx4 [ P1x P1y P2x P2y ]
	"""
	IDList    = [int(oneInfo[1])   for oneInfo in WALL]
	P1xList    = [float(oneInfo[2]) for oneInfo in WALL]
	P1yList    = [float(oneInfo[3]) for oneInfo in WALL]
	P2xList    = [float(oneInfo[4]) for oneInfo in WALL]
	P2yList    = [float(oneInfo[5]) for oneInfo in WALL]

	WALLId=np.matrix(IDList).T
	WALLP1x=np.matrix(P1xList).T
	WALLP1y=np.matrix(P1yList).T
	WALLP2x=np.matrix(P2xList).T
	WALLP2y=np.matrix(P2yList).T
	WALLP1P2xyxyN4 = np.hstack((WALLP1x, WALLP1y, WALLP2x, WALLP2y))
	# print('WALLP1P2xyxyN4', WALLP1P2xyxyN4)
	return WALLId, WALLP1P2xyxyN4


def ContactBondListStrToNumpyArray(CONTACT, BOND):
	"""
	转换为numpy数据类型
	输入参数：
	[1]CONTACT  接触信息n x [ id1  id2  Fn  Fs   globalFx   globalFy ...]
	[2]BOND     粘结信息n x [ id1  id2  Fn  Fs   globalFx   globalFy ...]
	输出参数：
	[1]CONTACTId1Id2N2    nx2 [id1 id2]
	[2]BONDId1Id2N2       nx2 [id1 id2]
	[3]BONDFnN1           nx1 [Fn]
	"""
	CONTACTId1List  = [int(oneInfo[0]) for oneInfo in CONTACT]
	CONTACTId2List  = [int(oneInfo[1]) for oneInfo in CONTACT]
	
	BONDId1List  = [int(oneInfo[0]) for oneInfo in BOND]
	BONDId2List  = [int(oneInfo[1]) for oneInfo in BOND]
	BONDFnList   = [float(oneInfo[2]) for oneInfo in BOND]
	

	CONTACTId1=np.matrix(CONTACTId1List).T
	CONTACTId2=np.matrix(CONTACTId2List).T
	CONTACTId1Id2N2 = np.hstack((CONTACTId1, CONTACTId2))
	
	BONDId1=np.matrix(BONDId1List).T
	BONDId2=np.matrix(BONDId2List).T
	BONDId1Id2N2 = np.hstack((BONDId1, BONDId2))
	
	BONDFnN1=np.matrix(BONDFnList).T

	return CONTACTId1Id2N2,BONDId1Id2N2,BONDFnN1
	
#def xy_move( WALLP1x, WALLP1y, WALLP2x, WALLP2y, BALLUx, BALLUy, xmove, ymove):
def xy_move( WALLP1P2xyxyN4, BALLxyN2, xmove, ymove):
	"""
	输入参数：
	[1] WALLP1P2xyxyN4  墙体信息 nx4 [P1x P1y P2x P2y]
	[1] BALLxyN2  颗粒信息 nx2 [x y]
	[2] xmove 颗粒坐标x方向偏移量
	[3] ymove 颗粒坐标y方向偏移量
	"""
	WALLP1P2xyxyN4 = WALLP1P2xyxyN4 + np.mat([[xmove,ymove,xmove,ymove]])
	BALLxyN2 = BALLxyN2 + np.mat([[xmove,ymove]])
	return WALLP1P2xyxyN4, BALLxyN2



def resource_path(relative_path):
	"""
	生成资源文件目录访问路径
	说明： pyinstaller工具打包的可执行文件，运行时sys。frozen会被设置成True
		  因此可以通过sys.frozen的值区分是开发环境还是打包后的生成环境

	打包后的生产环境，资源文件都放在sys._MEIPASS目录下
	修改main.spec中的datas，
	如datas=[('res', 'res')]，意思是当前目录下的res目录加入目标exe中，在运行时放在零时文件的根目录下，名称为res
	"""
	if getattr(sys, 'frozen', False):
		base_path = sys._MEIPASS
	else:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)


def GetColormapFile(colormap,VBOXscriptDir):
	"""
	获得 colormap 文件
	输入参数：
	[1] colormap  指定颜色配置文本文件路径，默认为'default'，格式为10x3的矩阵，对应十个RGB值．
	输出参数：
	[1] colormapfile  颜色配置文本文件路径
	"""
	if (colormap == 'default') :
		colormapfile=VBOXscriptDir+'/res/ColorRicebal.txt'
		my_file = Path(colormapfile)
		if (not my_file.exists()):
			#print("文件不存在，***colormapfile:",colormapfile)
			# 指定的文件存在	
			colormapfile = resource_path(os.path.join("res","ColorRicebal.txt"))
		
	else:
	#默认取值见https://doc.geovbox.com/zdem/color/．建议直接制定该文件的绝对路径或者相对路径，
	#如--colormap=/home/zhangsan/MyColorMap.txt或--colormap=./ＭyColorMap.txt．
	#如果仅指定文件名，如--colormap=ＭyColorMap.txt，搜索顺序为 当前目录 > --dir指定的目录 > Home．")
		colormapfile=colormap
		#print("1:", colormapfile)
		if ( os.path.isfile(colormapfile) == False ):
			colormapfile=DataDir+colormap
			if ( os.path.isfile(colormapfile) == False ):
				colormapfile=os.path.join(os.environ['HOME'],colormap)
				if ( os.path.isfile(colormapfile) == False ):
					print("找不到", colormap)

	#print("colormap:", colormapfile)
	#with open(colormapfile) as f:
	#    lines = f.readlines()
	#    print(lines)
	#    f.close()

	return colormapfile








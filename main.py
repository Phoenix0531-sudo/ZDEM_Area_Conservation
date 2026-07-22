#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取 VBOX 计算结果，批量生成颗粒与 bond 的 jpg 图片，支持并行绘图。
"""

import logging
from concurrent.futures import ProcessPoolExecutor

import os, sys, getopt, time
import os.path #判断文件是否存在
import matplotlib.ticker as ticker
#import multiprocessing

import zdemio
import zdemplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import checkLicense

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

logger = logging.getLogger('test_logger')
logger.setLevel(logging.WARNING)  #设置默认的日志级别 CRITICAL > ERROR > WARNING > INFO > DEBUG
#创建StreamHandler对象
sh = logging.StreamHandler()
#StreamHandler对象自定义日志级别
sh.setLevel(logging.INFO)
#StreamHandler对象自定义日志格式
#sh.setFormatter(formatter)
sh.flush()
logger.addHandler(sh)  #logger日志对象加载StreamHandler对象

softwareName=sys.argv[0]
version = '2.2'

VBOXscriptDir=sys.path[0]
sys.path.append(VBOXscriptDir)
total_list = []
#print ("VBOXscriptDir",VBOXscriptDir)
#print ("参数个数：",len(sys.argv))

#reg=checkLicense.register(version,VBOXscriptDir)
#reg.checkAuthored()

#print ('参数个数为:', len(sys.argv))
#print ('参数列表:', str(sys.argv))
if (len(sys.argv) < 2):
	zdemio.usage(softwareName)
	sys.exit()

opts, args = getopt.getopt(sys.argv[1:], "hv",\
longopts=['dir=','xmax=','ymax=','xmove=','ymove=','xmin=','ymin=',\
'major_locator=','minor_locator=','fontsize=','max_workers=','dpi=',\
'linewidth=','pagesize=','leftshow=','rightshow=','bottomshow=','topshow=',\
'wallshow=','colormap=','surfaceshow=','bondplot=','ballplot='])


input_file=""
output_file=""
DataDir=""
xmax=1000000000.0
ymax=1000000000.0
xmaxdefine='false'
ymaxdefine='false'
xmove=0.0
ymove=0.0
xmin=0.0
ymin=0.0
xmindefine='false'
ymindefine='false'
major_locator=10000.0
minor_locator=1000.0
fontsize=9
max_workers = 4
#print("max_workers:%d" %(max_workers) )

dpi=600
linewidth=0.5
pagesize=14
topshow='true'
rightshow='true'
bottomshow='true'
leftshow='true'
wallshow='true'
surfaceshow= 'false'
colormap='default'
bondplot='false'
ballplot='true'

for op, value in opts:
	if op == "-h":
		zdemio.usage(softwareName)
		sys.exit()
	elif op == "-v":
		print ("%s" %(version))
		sys.exit()
	elif op == "--dir":
		DataDir = value
		print ("DataDir", DataDir)
	elif op == "--xmax":
		xmax = float(value)
		xmaxdefine='true'
	elif op == "--ymax":
		ymax = float(value)
		ymaxdefine='true'
	elif op == "--xmove":
		xmove = float(value)
	elif op == "--ymove":
		ymove = float(value)
	elif op == "--xmin":
		xmin = float(value)
		xmindefine='true'
	elif op == "--ymin":
		ymin = float(value)
		ymindefine='true'
	elif op == "--major_locator":
		major_locator = float(value)
	elif op == "--minor_locator":
		minor_locator = float(value)
	elif op == "--fontsize":
		fontsize = float(value)
	elif op == "--max_workers":
		max_workers = int(value)
	elif op == "--dpi":
		dpi = int(value)
	elif op == "--linewidth":
		linewidth = float(value)
	elif op == "--pagesize":
		pagesize = float(value)
	elif op == "--topshow":
		topshow=value
	elif op == "--rightshow":
		rightshow=value
	elif op == "--bottomshow":
		bottomshow=value
	elif op == "--leftshow":
		leftshow=value
	elif op == "--wallshow":
		wallshow=value
	elif op == "--surfaceshow":
		surfaceshow=value
	elif op == "--colormap":
		colormap=value
	elif op == "--bondplot":
		bondplot=value
	elif op == "--ballplot":
		ballplot=value

#颜色查询
colormapfile= zdemio.GetColormapFile(colormap,VBOXscriptDir)
logger.info("colormapfile:%s" %(colormapfile) )

flist = []
plt.close('all')
ColorList, ColorMap = zdemplot.get_color_map(colormapfile)
#get <*.dat> file
VBOXfile= zdemio.get_file_list(DataDir, FileNamePrefix='all_', FileNameSuffix='.dat')
def compute_polygon_area(points):
    point_num = len(points)
    if(point_num < 3): return 0.0
    s = points[0][1] * (points[point_num-1][0] - points[1][0])

    for i in range(1, point_num):
        s += points[i][1] * (points[i-1][0] - points[(i+1)%point_num][0])
    return abs(s/2.0)

def read_and_gen_fig(file):
    
	print("read file:%s"%(file),flush=True)
	WALL,BALL,CONTACT,BOND,CurrentStep, Group=zdemio.read_data(file)
	test = []
	lef_wall = []
	rig_wall = []
	
	top_wall_left_x = float(WALL[7][4])
	top_wall_left_y = float(WALL[7][5])
	top_wall_right_x = float(WALL[7][2])
	top_wall_right_y = float(WALL[7][3])
	top_wall_left_y1 = float(WALL[8][5])
 
	bottom_wall_left_x = float(WALL[4][2])
	bottom_wall_left_y = float(WALL[4][3])
	bottom_wall_left_x1 = float(WALL[5][2])
	bottom_wall_left_y1 = float(WALL[5][3])
	bottom_wall_right_x = float(WALL[4][4])
	bottom_wall_right_y = float(WALL[4][5])
	bottom_wall_right_x1 = float(WALL[6][4])
	bottom_wall_right_y1 = float(WALL[6][5])
 
	area1 = (bottom_wall_right_x - bottom_wall_left_x1) * (bottom_wall_left_y - bottom_wall_left_y1)
	area2 = (top_wall_right_x - top_wall_left_x) * (top_wall_left_y1 - top_wall_left_y)
	total_area = area1 + area2
	total_list.append(total_area)
	
	# with open(r'E:\scientific_research\project\test\data\area_subtract.txt', 'a') as file:
	# 	file.write(str(total_area))
	# 	file.write('\n')


	
	for i in range(len(Group)):
		
		if Group[i][1] == 'lef_wall':
			for j in range(len(BALL)):
				if BALL[j][1] == Group[i][0]:
					test.append(BALL[j])
					lef_wall.append(BALL[j])
			
		if Group[i][1] == 'rig_wall':
			for j in range(len(BALL)):
				if BALL[j][1] == Group[i][0]:
					test.append(BALL[j])
					rig_wall.append(BALL[j])


	BALL = test
	Ball_position = []
	# Ball_position.append([float(bottom_wall_left_x), float(bottom_wall_left_y)])
	
	for k in range(len(lef_wall)):
		Ball_position.append([float(lef_wall[k][2]), float(lef_wall[k][3])])
	# Ball_position.append([float(top_wall_left_x), float(top_wall_left_y)])
	# Ball_position.append([float(top_wall_right_x), float(top_wall_right_y)])

	for k in range(len(rig_wall)):
		Ball_position.append([float(rig_wall[k][2]), float(rig_wall[len(rig_wall) - 1 - k][3])])
	# Ball_position.append([float(bottom_wall_right_x), float(bottom_wall_right_y)])

	filename = file.split('\\')[5].split('.')[0]
	with open(r'E:\scientific_research\project\test\data\{}.txt'.format(filename), 'a') as file:
		for i in range(len(Ball_position)):
			file.write(str(Ball_position[i][0]) + ',' +str(Ball_position[i][1]))
			file.write('\n')
	
	# print(Ball_position)
	# 
	#print(compute_polygon_area(Ball_position))
	#List to array
	BALLIdN1, BALLxyN2, BALLRadN1, BALLColor = zdemio.BallListStrToNumpyArray(BALL)
	WALLIdN1, WALLP1P2xyxyN4 = zdemio.WallListStrToNumpyArray(WALL)
	
	WALLP1P2xyxyN4, BALLxyN2 = zdemio.xy_move(WALLP1P2xyxyN4, BALLxyN2, xmove, ymove)
	wbleft,wbright,wbbottom,wbtop = zdemplot.search_domain(WALLP1P2xyxyN4, BALLxyN2, BALLRadN1)
	#print(wbleft,wbright,wbbottom,wbtop )
	
	#plot ball
	if ballplot =='true':
		logger.info("plot ball...")
		tic = time.time()
		figball=plt.figure(1)
	#	ax = subplot(111,aspect='equal')
		axball=plt.gca()
		#bleft,bright,bbottom,btop = zdemplot.plot_ball(fig,ax,Ball,ColorList)
		zdemplot.plot_ball(figball,axball,BALLxyN2, BALLRadN1, BALLColor, ColorList)
		#print(wbleft,wbright,wbbottom,wbtop )
		
		#print('wallshow',wallshow)
		if (wallshow == 'true'): 
			zdemplot.plot_wall(figball,axball,WALLP1P2xyxyN4,ColorList,linewidth=linewidth)
		if (surfaceshow == 'true'): 
			zdemplot.plot_surface(figball,axball,BALLxyN2, BALLRadN1,linewidth=linewidth)
		
		#set figure
		zdemplot.zdem_fig_set(figball,axball,xmaxdefine, ymaxdefine, xmindefine, ymindefine, 
							xmin,xmax,ymin,ymax,
							wbleft,wbright,wbbottom,wbtop,
							leftshow,rightshow,bottomshow,topshow,
							major_locator,minor_locator,fontsize,linewidth,pagesize)
		
		VBOXfileJPG = file.replace('.dat','.jpg')
		figball.savefig(VBOXfileJPG,dpi=dpi, bbox_inches="tight")#, pad_inches=0.0)
		#fig.savefig(figName+'.pdf',dpi=300, bbox_inches="tight")
		plt.close(figball)
		
		toc = time.time()
		logger.info('used {:.5}s'.format(toc-tic))

	#plot bond
	if bondplot =='true':
		logger.info("plot bond...")
		
		CONTACTId1Id2N2,BONDId1Id2N2,BONDFnN1 =\
								zdemio.ContactBondListStrToNumpyArray(CONTACT, BOND)

		tic = time.time()
		allnum = cmd_bondplot(file,CurrentStep,BALLIdN1, BALLxyN2,BALLRadN1,\
						WALLP1P2xyxyN4,ColorList,\
						CONTACTId1Id2N2,BONDId1Id2N2,BONDFnN1,\
						xmaxdefine, ymaxdefine, xmindefine, ymindefine,\
						xmin,xmax,ymin,ymax,\
						wbleft,wbright,wbbottom,wbtop,\
						leftshow,rightshow,bottomshow,topshow,\
						major_locator,minor_locator,fontsize,linewidth,pagesize)
		
		toc = time.time()
		logger.info('used {:.5}s'.format(toc-tic))

		#allnum=[0,1,2,3,4]
		return allnum
	
def cmd_bondplot(file,CurrentStep,BALLIdN1, BALLxyN2,BALLRadN1,
				WALLP1P2xyxyN4,ColorList,
				CONTACTId1Id2N2,BONDId1Id2N2,BONDFnN1,
				xmaxdefine, ymaxdefine, xmindefine, ymindefine, 
				xmin,xmax,ymin,ymax,
				wbleft,wbright,wbbottom,wbtop,
				leftshow,rightshow,bottomshow,topshow,
				major_locator,minor_locator,fontsize,linewidth,pagesize):
	
	figbond=plt.figure(2)
	axbond=plt.gca()
#	FnGEZero,FnLTZero = 0,0
	FnGEZero,FnLTZero = zdemplot.plot_contactbond(figbond, axbond,
						BALLIdN1, BALLxyN2,
						CONTACTId1Id2N2,BONDId1Id2N2,BONDFnN1,
						linewidth=linewidth)

	logger.debug('wallshow')
	if (wallshow == 'true'): 
		zdemplot.plot_wall(figbond,axbond,WALLP1P2xyxyN4,ColorList,linewidth=linewidth)
	if (surfaceshow == 'true'): 
		zdemplot.plot_surface(figbond,axbond,BALLxyN2, BALLRadN1,linewidth=linewidth)

	#set figure
	zdemplot.zdem_fig_set(figbond,axbond,xmaxdefine, ymaxdefine, xmindefine, ymindefine, 
						xmin,xmax,ymin,ymax,
						wbleft,wbright,wbbottom,wbtop,
						leftshow,rightshow,bottomshow,topshow,
						major_locator,minor_locator,fontsize,linewidth,pagesize)

	VBOXfileJPG = file.replace('.dat','.jpg')
	VBOXfileJPG = VBOXfileJPG.replace('all','bond')
	figbond.savefig(VBOXfileJPG,dpi=dpi, bbox_inches="tight")#, pad_inches=0.0)
	plt.close(figbond)
	#print(file1[-10:])

	# step contact_num bond_num pushnum(blue) pullnum(red)
	return int(CurrentStep),CONTACTId1Id2N2.shape[0],BONDId1Id2N2.shape[0],FnGEZero,FnLTZero


allnum=[]

max_workers=min(max_workers,len(VBOXfile))
print("parallel num:",max_workers)
print("file num:",len(VBOXfile))
if __name__ == '__main__' :
	with ProcessPoolExecutor(max_workers=max_workers) as executor:
		VBOXfileList= VBOXfile
		allnum=executor.map(read_and_gen_fig, VBOXfileList)
	

#test
#for file in VBOXfile:
#	allnum.append(read_and_gen_fig(file))
#print("allnum",allnum,flush=True)

#write contact and bond num to file
if bondplot =='true':
	fileContactBondName='contactbond_num.txt'
	allnum=list(allnum)
	logger.info(allnum)
	allnum=sorted(allnum,key=lambda x:x[0])
	logger.info(allnum)
	filecb = os.path.join(DataDir,fileContactBondName)
	#print('filecb:',filecb)
	with open(filecb,"w+") as f:
		f.write("#{0:>15s} {1:>15s} {2:>15s} {3:>15s} {4:>15s} \n".format(\
			"step","contact","bond","push(blue)","pull(red)"))
		#f.write('# step contact_num bond_num pushnum(blue) pullnum(red)'+"\n")
		for line in allnum:
			#line = " ".join('%9s'%i for i in line)
			#f.write(line+"\n")
			f.write(" {0[0]:>15d} {0[1]:>15d} {0[2]:>15d} {0[3]:>15d} {0[4]:>15d}\n".format(line) )




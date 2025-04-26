#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2022/03/28 v2.2 beta 李长圣 == 广播查找索引，将创建 n个颗粒m个bond的超级大矩阵，导致内存溢出
	1. plot_contactbond()中Id1Id2ToIndex1Index2()
2022/03/26 v2.2 beta 李长圣 clear code rubbish, numpy array -> matrix
2022/03/23 v2.2 beta 李长圣 修复plotbond中，--xmax=40000 --ymax=10000，不起作用问题。
    1. 修改数据为numpy array
    2. 改为EllipseCollection 和 LineCollection绘制大量圆和线段，速度提高~9倍
    3. 增加 --ballplot 默认为ture
2019/08/26
李长圣 @ 东华理工大学
实现并行绘图，增加 --xmove= --ymove=

2019/01/07
李长圣 @ 南京大学

功能：
读取VBOX计算结果，生成jpg图片
plot ball to jpg

输入参数：
[1] DataDir  VBOX计算结果所在目录

输出：
[1] jpg格式文件

例如：
./main.py --dir=./example 
./main.py --dir=./example --xmax=40000 --ymax=10000 --xmove=-1000.0 --ymove=-1000.0 --xmin=0.0 --ymin=0.0 --major_locator=10000.0 --minor_locator=1000.0 --fontsize=12 --pagesize=14 --topshow=false --wallshow=true --colormap=./mycolormap.txt --bondplot=false --ballplot=true
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

#2022-03-25 add logging
#logging.basicConfig(level=logging.INFO)
#创建一个logger日志对象
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

#2021-04-24
#添加软件版本号
softwareName=sys.argv[0]
version = '2.2'

VBOXscriptDir=sys.path[0]
sys.path.append(VBOXscriptDir)
#print ("VBOXscriptDir",VBOXscriptDir)
#print ("参数个数：",len(sys.argv))

#2021-04-24
#验证许可证
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
#2020-12-29 lichangsheng 
#默认线程数改为cpu核心数
#max_workers=24
#是当前节点的核心数，不是可用核心数
#max_workers = multiprocessing.cpu_count()

#2021-06-17 如果#SBATCH -c 1分配一个核给程序，srun -n 1 zdem2jpg --dir=./data
#会开辟很多线程，然而slurm仅仅分配给程序一个核，所以各个线程存在竞争，
#弹出Out Of Memory错误，无法绘图。
#采用multiprocessing.cpu_count() slurm无法获取分配的核心数
#改为获取可用核心数
pid=0 #当前进程
import multiprocessing
try:
    max_workers = len(os.sched_getaffinity(pid))
except AttributeError:
    # Windows系统使用CPU核心数
    max_workers = multiprocessing.cpu_count()

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
if len(sys.argv) < 2:
	usage()
	os._exit(0)

#颜色查询
colormapfile= zdemio.GetColormapFile(colormap,VBOXscriptDir)
logger.info("colormapfile:%s" %(colormapfile) )

flist = []
plt.close('all')
ColorList, ColorMap = zdemplot.get_color_map(colormapfile)
#get <*.dat> file
VBOXfile= zdemio.get_file_list(DataDir, FileNamePrefix='all_', FileNameSuffix='.dat')

def read_and_gen_fig(file):
	print("read file:%s"%(file),flush=True)
	WALL,BALL,CONTACT,BOND,CurrentStep=zdemio.read_data(file)
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

#2020-07-27 李长圣　分离绘制颗粒和绘制粘结
#2019-08-26 实现并行绘图 max_workers=5
#开辟的进程数应小于文件数
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



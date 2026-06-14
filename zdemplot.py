# -*- coding: utf-8 -*-
"""
绘制颗粒及墙体
"""

import os
import shutil
import numpy as np
import time
import matplotlib.ticker as ticker
#from pylab import *
from math import ceil

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.collections import EllipseCollection
from matplotlib import colors as mcolors
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

def get_color_map(filename):
	"""获取颜色映射表"""
	xfile = open(filename, "r")#, encoding = 'utf-8')
	colorlist = []
	for line in xfile:
		ltmp = line.split()
		#print (ltmp, '\n')
		for i in range(len(ltmp)):
			ltmp[i] = float(ltmp[i])
		colorlist.append(ltmp)
	xfile.close()
	
	colormap={}
	colormap['light gray']  = (colorlist[0],0)
	colormap['green']       = (colorlist[1],1)
	colormap['yellow']      = (colorlist[2],2)
	colormap['red']         = (colorlist[3],3)
	colormap['white']       = (colorlist[4],4)
	colormap['black']       = (colorlist[5],5)
	colormap['medium gray'] = (colorlist[6],6)
	colormap['blue']        = (colorlist[7],7)
	colormap['green blue']  = (colorlist[8],8)
	colormap['violet']      = (colorlist[9],9)
	return colorlist,colormap

def plot_ball(fig, ax, BALLxyN2, BALLRadN1, BALLColorN1, ColorList):
	"""
	输入参数：
	[1] fig  
	[2] ax
	[3] BALLxyN2   nx2
	[4] BALLRadN1 nx1
	[5] BALLColorN1 nx1
	[6] ColorList
		[0.85 0.85 0.85 
		 0.00 1.00 0.00
		 1.00 1.00 0.00
		 1.00 0.00 0.00 
		 0.90 0.90 0.90 
		 0.15 0.15 0.15 
		 0.50 0.50 0.50 
		 0.00 0.00 1.00 
		 0.00 1.00 1.00 
		 1.00 0.00 1.00]
	"""
	
	ww = BALLRadN1 * 2.0
	hh = ww
	#print("ww.shape",ww.shape)
	aa = np.zeros(ww.shape)
	XY = BALLxyN2
	
	# set color
	#list(n) 
	#list[0]=(r,g,b,t)
	# ...
	#list[n]=(r,g,b,t)
	facecolors = [ tuple(ColorList[c[0,0]]) for c in BALLColorN1 ]# c=[r,g,b,t]
	
	circles = EllipseCollection(ww,hh,aa,
								units='x',offsets=XY,
								transOffset=ax.transData,
								edgecolors='none',
								facecolors=facecolors,
								linestyles='solid')
	ax.add_collection(circles)

def search_domain(WALLP1P2xyxyN4, BALLxyN2, BALLRad):

	wallNum=WALLP1P2xyxyN4.shape[0]
	ballNum=BALLxyN2.shape[0]

	if (wallNum!=0):
		Wleft,Wright,Wbottom,Wtop = search_domain_wall(WALLP1P2xyxyN4)
		#print("w",Wleft,Wright,Wbottom,Wtop)
	if (ballNum!=0):
		Bleft,Bright,Bbottom,Btop = search_domain_ball(BALLxyN2, BALLRad)
		#print("b",Bleft,Bright,Bbottom,Btop)
	
	if (wallNum!=0):
		if (ballNum!=0):
			return min(Wleft,Bleft), max(Wright,Bright), min(Wbottom,Bbottom), max(Wtop,Btop)
		else:
			return Wleft, Wright,Bright, Wbottom, Wtop
	else:
		if (ballNum!=0):
			return Bleft, Bright, Bbottom, Btop
		else:
			return 0.0,1.0,0.0,1.0

def search_domain_wall(WALLP1P2xyxyN4):

	P1P2xyxymin = WALLP1P2xyxyN4.min(axis=0) # [P1xmin P1ymin P2xmin P2ymin]
	P1P2xyxymax = WALLP1P2xyxyN4.max(axis=0) # [P1xmax P1ymax P2xmax P2ymax]

	left   = min(P1P2xyxymin[0,0],P1P2xyxymin[0,2])
	right  = max(P1P2xyxymax[0,0],P1P2xyxymax[0,2])
	bottom = min(P1P2xyxymin[0,1],P1P2xyxymin[0,3])
	top    = max(P1P2xyxymax[0,1],P1P2xyxymax[0,3])
	
	return left,right,bottom,top

def search_domain_ball(BALLxyN2, BALLRad):

	leftbottom = (BALLxyN2-BALLRad).min(axis=0)
	righttop = (BALLxyN2+BALLRad).max(axis=0)
	
	left = leftbottom[0,0]
	bottom = leftbottom[0,1]
	
	right = righttop[0,0]
	top = righttop[0,1]
	
	return left,right,bottom,top
	
def plot_wall(fig, ax, WALLP1P2xyxyN4, ColorList,linewidth=1):

	WALLsegs=[np.row_stack([P1P2xyxy[0,0:2], P1P2xyxy[0,2:4]]) for P1P2xyxy in WALLP1P2xyxyN4 ]
	#set color
#	colors = [mcolors.to_rgba(c) 
#          for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]

	wallNum=WALLP1P2xyxyN4.shape[0]
	#print("wallNum",wallNum)
	WALLColors=np.zeros((wallNum,4))
	WALLColors=WALLColors+np.array([0.0,0.0,0.0,1.0]) #black
	#print("WALLColors",WALLColors)
	
	WALLColorList=[tuple(c) for c in WALLColors ]
	#facecolors = [ tuple(ColorList[c]) for c in BALLColor ]# c=[r,g,b,t]
	
	WALLline_segments = LineCollection(WALLsegs, linewidths=linewidth, colors=WALLColorList, linestyles='solid')
	ax.add_collection(WALLline_segments)
#	print("WALLColorList",WALLColorList)

def plot_surface(fig, ax, BALLxyN2, BALLRadN1, linewidth=1):
	"""
	输入参数：
	[1] fig  
	[2] ax
	[3] BALLxyN2   nx2
	[4] BALLRadN1  nx1
	"""
	dx=200
	dy=5000
	
	left   = (BALLxyN2[:,0]-BALLRadN1).min()
	right  = (BALLxyN2[:,0]+BALLRadN1).max()
	
	nx= int(ceil((right - left)/dx))
	ycol=np.zeros((2,nx))
	#print("BALLUx.shape[0]:",BALLUx.shape[0])
	for i in range(BALLxyN2.shape[0]):
	#for Ux,Uy,rad in BALLUx, BALLUy, BALLRadN1:
		Ux,Uy,rad = BALLxyN2[i,0], BALLxyN2[i,1], BALLRadN1[i]
		index = int(ceil((Ux-left)/dx))
		if(index>0):
			index=index-1
		if(Uy > ycol[0,index]):
			ycol[0,index] = Uy+rad
			ycol[1,index] = i #记住颗粒index
	LineX=np.zeros(nx)
	LineY=np.zeros(nx)
	for i in range(nx):
		LineX[i]=dx*i+left
		if i>0 and i<(nx-1):
			if abs(ycol[0,i] - ycol[0,i-1]) <dy and abs(ycol[0,i+1] - ycol[0,i])<dy:
				LineY[i]=ycol[0,i]*0.5+ycol[0,i-1]*0.25+ycol[0,i+1]*0.25
			else:
				LineY[i]=ycol[0,i]
		else:
			LineY[i]=ycol[0,i]
	ax.add_line(Line2D(LineX, LineY , linewidth=linewidth, color='black'))

def plot_contactbond(fig, ax, BALLIdN1, BALLxyN2,
						CONTACTId1Id2N2,BONDId1Id2N2,BONDFnN1,
						linewidth=0.2):
	"""
	将 BOND Id1Id2 映射到 BALL 索引，绘制 contact 线段和 bond 线段。
	"""
	BALLIdN1=BALLIdN1.T #列变成行
	
#	#plot contact

	# 将[id1 id2]转换为[index1 index2]
	CONTACTIDId1Id2index = Id1Id2ToIndex1Index2(BALLIdN1,CONTACTId1Id2N2)
	
	CONTACTXYid1 = BALLxyN2[CONTACTIDId1Id2index[:,0],:] # nx2 [x,y]
	CONTACTXYid2 = BALLxyN2[CONTACTIDId1Id2index[:,1],:]

	CONTACTsegs=[np.vstack((id1xy, id2xy)) for id1xy,id2xy in zip(CONTACTXYid1,CONTACTXYid2) ]
	
	#color
	contactnum=CONTACTId1Id2N2.shape[0]
	
	CONTACTColors=np.zeros((contactnum,4))
	CONTACTColors=CONTACTColors+np.array([0.0,0.0,0.0,1.0]) #black
	CONTACTColorList=[tuple(c) for c in CONTACTColors ]
	
	CONTACTline_segments = LineCollection(CONTACTsegs, linewidths=linewidth, colors=CONTACTColorList, linestyles='solid')
	ax.add_collection(CONTACTline_segments)

	#plot bond
	bondnum=BONDFnN1.shape[0]
	
	# 将[id1 id2]转换为[index1 index2]
	BONDId1Id2index = Id1Id2ToIndex1Index2(BALLIdN1,BONDId1Id2N2)

	BONDXYid1 = BALLxyN2[BONDId1Id2index[:,0],:] # nx2  [x, y]
	BONDXYid2 = BALLxyN2[BONDId1Id2index[:,1],:] # nx2  [x, y]
	
	segs=[np.vstack((id1xy, id2xy)) for id1xy,id2xy in zip(BONDXYid1,BONDXYid2) ]
	
	#color
	FnLTZero=0 #Fn<0 red
	FnGEZero=0 #Fn>=0 blue
#	colors = [mcolors.to_rgba(c) 
#          for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]
	indexRed=np.where(BONDFnN1<0)
	indexBlue=np.where(BONDFnN1>=0)
	FnLTZero=indexRed[0].shape[0] #Fn<0 red
	FnGEZero=indexBlue[0].shape[0] #Fn>=0 blue
	
	Colors=np.zeros((bondnum,4))
	Colors[indexRed,:]=np.array([1.0,0.0,0.0,1.0]) #red
	Colors[indexBlue,:]=np.array([0.0,0.0,1.0,1.0]) #blue
	ColorList=[tuple(c) for c in Colors ]
	
	line_segments = LineCollection(segs, linewidths=linewidth, colors=ColorList, linestyles='solid')
	ax.add_collection(line_segments)

	return FnGEZero,FnLTZero

def Id1Id2ToIndex1Index2(BALLIdN1,Id1Id2N2):
	"""将 [id1 id2] 转换为 [index1 index2]，逐行查找避免广播大矩阵内存溢出。"""
	bondnum=Id1Id2N2.shape[0]
	Id1Id2indexN2=np.mat(np.zeros_like(Id1Id2N2,dtype=int)) # nx2
	for i in np.arange(bondnum):
		id1id2=Id1Id2N2[i,:].T #取出一个bond， [id1, id2]
		index1index2 = np.where(BALLIdN1==id1id2)[-1]
		Id1Id2indexN2[i,:]=index1index2 #[index1 index2]
	
	return Id1Id2indexN2

def fig_set(fig):
	"""
	输入参数：
	[1] fig  
	"""

	#plt.plot(VBOXx,VBOXy,'.')
	plt.xlim(left=0.0)#, xmax = 0.16)
	#plt.xlim(right = 120)
	plt.ylim(bottom=0.0)
	plt.axis('equal')   #changes limits of x or y axis so that equal increments of x and y have the same length

	#plt.ylim(top =20)
	#plt.show()
	wi,hi=fig.get_size_inches()
	#print("wi", wi, "hi",hi)
	wcm=8 #cm
	#hcm=
	winch=wcm/2.54
	hinch=winch/wi*hi
	#print("winch", winch, "hinch",hinch)
	fig.set_size_inches(w=winch,h=hinch)

def zdem_fig_set(fig,ax,xmaxdefine, ymaxdefine, xmindefine, ymindefine, 
				xmin,xmax,ymin,ymax,
				wbleft,wbright,wbbottom,wbtop,
				leftshow,rightshow,bottomshow,topshow,
				major_locator,minor_locator,fontsize,linewidth,pagesize):
	
	if (xmaxdefine=='true'):
		right  = xmax
	else:
		right=min(wbright,xmax)
	
	if (ymaxdefine=='true'):
		top  = ymax
	else:
		top  =min(wbtop,ymax)
		
	if (xmindefine=='true'):
		left  = xmin
	else:
		left=max(wbleft,xmin);
	
	if (ymindefine=='true'):
		bottom  = ymin
	else:
		bottom=max(wbbottom,ymin);
		
	#print(left,right,bottom,top)

	realticks=range(0, 400000, int(major_locator) )
	showticks= [str(x) for x in range(0, 400, int(int(major_locator)/1000) )]
	plt.xticks(realticks,showticks)
	plt.yticks(realticks,showticks)
	ax.xaxis.set_minor_locator(ticker.MultipleLocator(minor_locator))
	ax.yaxis.set_minor_locator(ticker.MultipleLocator(minor_locator))
	# 设置刻度字体大小
	plt.xticks(fontsize=fontsize)
	plt.yticks(fontsize=fontsize)
	plt.tick_params(labelsize=fontsize)
	###设置坐标轴的粗细
	ax.spines['bottom'].set_linewidth(linewidth);###设置底部坐标轴的粗细
	ax.spines['left'].set_linewidth(linewidth);####设置左边坐标轴的粗细
	ax.spines['right'].set_linewidth(linewidth);###设置右边坐标轴的粗细
	ax.spines['top'].set_linewidth(linewidth);####设置上部坐标轴的粗细
	#set 刻度线粗细 刻度线与标签的间隔
	ax.tick_params(which='both',width=linewidth, pad=1);

	#wi,hi=fig.get_size_inches()
	wi=right-left
	hi=top-bottom
#	print("wi", wi, "hi",hi)
#	hi=3.0
	wcm=pagesize #cm
	#hcm=
	winch=wcm/2.54
	hinch=winch/wi*hi
#	hinch=1
	#print("winch", winch, "hinch",hinch)
	fig.set_size_inches(w=winch,h=hinch)

	#plt.axis('equal')   #changes limits of x or y axis so that equal increments of x and y have the same length
#	plt.plot(VBOXx,VBOXy,'.')
	#print(left,right,bottom,top)
	plt.xlim(left=left)#, xmax = 0.16)
	plt.xlim(right=right)
	plt.ylim(bottom=bottom)
	plt.ylim(top=top)
	#去掉边框
	#print("topshow:",topshow)
	if (topshow=='false'): ax.spines['top'].set_visible(False)
	if (rightshow=='false'): ax.spines['right'].set_visible(False)
	if (bottomshow=='false'): ax.spines['bottom'].set_visible(False)
	if (leftshow=='false'): ax.spines['left'].set_visible(False)



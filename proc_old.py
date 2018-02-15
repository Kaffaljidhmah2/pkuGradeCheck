#coding:utf-8
from PIL import Image
from heapq import nlargest
import sys
import numpy as np

trainset=[]
show=False
parameter_k=10

def loadtrain():
	'''Load Training set'''
	s=open('trainset','r').read()
	u=s.split('\n')
	for i in u:
		out=i.split(' ')
		if (len(out)==11):
			trainset.append(out)


def geti(label):
	'''Get the egivector list'''
	file_name=label
	egset=[]
	im=Image.open(file_name)
	imd=np.array(im)
	count=[0 for i in range(16)]
	for i in imd:
		for j in i:
			count[j]+=1
	a=nlargest(5,count)

	for k in range(1,5):
		evector=[0 for ll in range(len(imd))]
		leftest=40
		flip=0
		for i in range(len(imd)):
			for j in range(len(imd[0])):
				if count[imd[i][j]]==a[k]:
					if flip==0:
						evector[i]*=10
						evector[i]+=1
						flip=1
					else:
						evector[i]+=1
					if leftest>j:
						leftest=j
				else:
					flip=0
		while evector[0]==0:
			del evector[0]
		while evector[-1]==0:
			del evector[-1]
		egset.append([evector,leftest])
	egset.sort(key=lambda x:x[1])
	if show:
		for i in range(len(imd)):
			for j in range(len(imd[0])):
				if count[imd[i][j]] in a[1:]:
					print('*',end='')
				else:
					print(' ',end='')
			print()
	return [x[0] for x in egset]


def knn(evector,k):
	'''Get the k-Nearest Neighbour of the egivector'''
	dis=[]
	for i in range(len(trainset)):
		x1=np.array(trainset[i][:-1],dtype=int)
		x2=np.array(evector)
		dis.append([i,np.linalg.norm(x2-x1,1)])
	dis.sort(key=lambda x:x[1])
	u=[]
	for i in [i[0] for i in dis[:k]]:
		u.append(trainset[i][10])
	return u


def getbest(lst):
	'''sort out what character is using knn'''
	u=dict()
	for i in range(len(lst)):
		if lst[i] in u:
			u[lst[i]]+=len(lst)-i
		else:
			u[lst[i]]=len(lst)-i
	return max(u,key=u.get)

def autoget(label):
	if len(trainset)==0:
		loadtrain()
	res=''
	e=geti(label)
	if len(e)!=4:
		return 'error'
	for i in e:
		if len(i)==10:
			res+=getbest(knn(i,parameter_k))
			if show:
				print(knn(i,parameter_k))
		else:
			return 'error'
	return res

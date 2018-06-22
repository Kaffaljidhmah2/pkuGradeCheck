import numpy as np
import os
from PIL import Image
from heapq import nlargest

cor_pp=dict()
cor_pp_big=dict()
f=open('valset_big','r').read().strip()
for item in f.split('\n'):
    rows=item.strip().split(' ')
    label=rows[0]
    h,w=int(rows[1]),int(rows[2])
    element=[int(i.strip()) for i in rows[3:]]
    cor_pp_big[label]=np.array(element)
    cor_pp_big[label].resize((h,w))
f=open('valset','r').read().strip()
for item in f.split('\n'):
    rows=item.strip().split(' ')
    label=rows[0]
    h,w=int(rows[1]),int(rows[2])
    element=[int(i.strip()) for i in rows[3:]]
    cor_pp[label]=np.array(element)
    cor_pp[label].resize((h,w))

def loadimage(url):
    return np.array(Image.open(url))

def spi(e):
    count=[0 for i in range(16)]
    for i in range(len(e)):
        for j in range(len(e[0])):
            count[e[i][j]]+=1
    a=nlargest(5,count)
    for i in range(len(e)):
        for j in range(len(e[0])):
            if count[e[i][j]] not in a:
                e[i][j]=count.index(a[0])
    c=[0,0,0,0]
    c[0],c[1],c[2],c[3]=e[:,0:12].copy(),e[:,8:20].copy(),e[:,17:29].copy(),e[:,25:37].copy()
    for l in range(4):
        count=[0 for tmpi in range(16)]
        for i in range(len(c[l])):
            for j in range(len(c[l][0])):
                count[c[l][i][j]]+=1
        a=nlargest(2,count)
        for i in range(len(c[l])):
            for j in range(len(c[l][0])):
                if count[c[l][i][j]]==a[1]:
                    c[l][i][j]=1
                else:
                    c[l][i][j]=0
    ee=[np.array(i,dtype=float) for i in c]
    return ee

def regular(e):
    e[e==0]=-1.0

#No zero-padding, stride=1
def convolve(graph,kernel):
    output_height=graph.shape[0]-kernel.shape[0]+1
    output_width=graph.shape[1]-kernel.shape[1]+1
    output=np.empty((output_height,output_width))
    for i in range(output_height):
        for j in range(output_width):
            output[i,j]=np.sum(graph[i:i+kernel.shape[0],j:j+kernel.shape[1]]*kernel)
    return output

def maxpool(feature):
    return np.max(feature,axis=0)

def autoget(url):
    im=loadimage(url)
    c=spi(im)
    code=''
    for l in range(4):
        newim=c[l]
        regular(newim)
        sheet=dict()
        for item in sorted(cor_pp.keys()):    
            pr=cor_pp[item]/np.sum(cor_pp[item])
            pr_big=cor_pp_big[item]/np.sum(cor_pp_big[item])
            res=maxpool(convolve(newim,pr))
            res_big=maxpool(convolve(newim,pr_big))
            sheet[item]=max(max(res),max(res_big))
        code+=max(sheet,key=lambda x : sheet[x])
    return code

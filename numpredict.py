# -*- coding: cp936 -*-
#使用kNN预测价格
from random import random,randint
import math

def wineprice(rating,age):
    peak_age=rating-50

    price=rating/2
    if age>peak_age:
        price=price*(5-(age-peak_age))
    else:
        price=price*(5*((age+1)/peak_age))
    if price<0:
        price=0
    return price

def wineset1():
    rows=[]
    for i in range(300):
        rating=random()*50+50
        age=random()*50

        price=wineprice(rating,age)
        price*=(random()*0.4+0.8)

        rows.append({'input':(rating,age),'result':price})
    return rows

def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)

def getdistances(data,vec1):
    distancelist=[]
    for i in range(len(data)):
        vec2=data[i]['input']
        distancelist.append((euclidean(vec1,vec2),i))
    distancelist.sort()
    return distancelist

def knnestimate(data,vec1,k=5):
    dlist=getdistances(data,vec1)
    avg=0.0

    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result']
    avg=avg/k
    return avg

def gaussian(dist,sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=5,weightf=gaussian):
    dlist=getdistances(data,vec1)
    avg=0.0
    totalweight=0.0

    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    avg=avg/totalweight
    return avg


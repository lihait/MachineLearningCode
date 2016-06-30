# -*- coding: cp936 -*-
#朴素贝叶斯分类器的实现
#运行
#reload(docclass)
#c1=docclass.naivebayes(docclass.getwords)
#docclass.sampletrain(c1)
#c1.classify('quick rabbit',default='unknown')
#构建训练样本
def sampletrain(c1):
    c1.train('Nobody owns the water.','good')
    c1.train('the quick rabbit jumps fences','good')
    c1.train('buy pharmaceuticals now','bad')
    c1.train('make quick money at the online casino','bad')
    c1.train('the quick brown fox jumps','good')
import re
import math
#从文本中提取特征
def getwords(doc):
    splitter=re.compile('\\W*')
    #根据非字母字典进行单词拆分
    words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    #只返回一组不重复的单词
    return dict([(w,1) for w in words])

#分类器
class classifier:
    def __init__(self,getfeatures):
        self.fc={}
        self.cc={}
        self.getfeatures=getfeatures
        #classifier.__init__(self,getfeatures)
        self.thresholds={}

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat]+=1

    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1

    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    def totalcount(self):
        return sum(self.cc.values())

    def categories(self):
        return self.cc.keys()

    def train(self,item,cat):
        features=self.getfeatures(item)
        for f in features:
            self.incf(f,cat)
        self.incc(cat)

    def fprob(self,f,cat):
        if self.catcount(cat)==0:
            return 0
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        basicprob=prf(f,cat)

        totals=sum([self.fcount(f,c) for c in self.categories()])

        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

    def classify(self,item,default=None):
        probs={}

        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat
                
        for cat in probs:
            if cat==best:
                continue
            if probs[cat]*self.getthreshold(best)>probs[best]:
                return default
            return best
            
class naivebayes(classifier):
        
    def docprob(self,item,cat):
        features=self.getfeatures(item)

        p=1
        for f in features:
            p*=self.weightedprob(f,cat,self.fprob)
        return p

    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob
        
    
        

import numpy as np
from django.shortcuts import render
import joblib
import pickle
from numpy import char
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, StandardScaler
from csv import DictWriter
from sklearn.metrics import accuracy_score

model=joblib.load(open('RandomForest.sav','rb'))
knn=pickle.load(open('KNN.sav','rb'))
svm=joblib.load(open('SVM.sav','rb'))


# Create your views here.
def home(request):
    return render(request,'inndex.html')

def enter(request):
    temp={}
    temp['Cardnum']=""
    temp['Merchnum']=""
    temp['Merch description']=''
    temp['Merch state']=''
    temp['Transtype']=""
    temp['Date']=""
    temp['Merch zip']=''
    temp['Amount']=""
    context={'temp':temp}
    return render(request,'form.html',context)

def test(): 
    x_test=pd.read_csv('x_test.csv')
    x_test=x_test.apply(LabelEncoder().fit_transform)
    x_test=StandardScaler().fit_transform(x_test)
    scoreval=model.predict(x_test)
    print(scoreval)
    y_test=pd.read_csv('y_test.csv')
    print(accuracy_score(y_test,scoreval)*100)


def predict(request):
    if request.method=='POST':
        temp={}
        temp['Cardnum']=int(request.POST.get('Cardnum'))
        temp['Date']=str(request.POST.get('Date'))
        temp['Merchnum']=str(request.POST.get('Merchnum'))
        temp['Merch description']=str(request.POST.get('Merch description'))
        temp['Merch state']=str(request.POST.get('Merch state'))
        temp['Merch zip']=float(request.POST.get('Merch zip'))
        temp['Transtype']=str(request.POST.get('Transtype'))
        temp['Amount']=float(request.POST.get('Amount'))
        print(temp)
        entered_data=pd.DataFrame({'x':temp}).transpose()
        print(entered_data)

    cols=['Cardnum','Date','Merchnum','Merch description','Merch state','Merch zip','Transtype','Amount']
   
    with open('x_train.csv', 'a+',newline='') as f:
        dict_writer= DictWriter(f, fieldnames=cols)
        print("*********************")
        dict_writer.writerow(temp)
        print(dict_writer)
        f.close()
    x=pd.read_csv('x_train.csv')
    print(x)
    x=x.apply(LabelEncoder().fit_transform)

    final=StandardScaler().fit_transform(x)
    df=pd.DataFrame(final,columns=['Cardnum','Date','Merchnum','Merch description','Merch state','Merch zip','Transtype','Amount'])
 
    scoreval1=model.predict(final[-1:])
    scoreval2=knn.predict(final[-1:])
    scoreval3=svm.predict(final[-1:])
    print (scoreval1)
    context={}
    context['scoredf1']=int(scoreval1)
    context['scoredf2']=int(scoreval2)
    context['scoredf3']=int(scoreval3)
    z=0
    o=0
    print(context)
    for i in context.values():
        if i==0:
            z=z+1
        else:
            o=o+1
    print(z)
    print(o)
    if z>o:
        fscore=0
    else:
        fscore=1
    result={}
    if fscore==0:
        result['score']="LEGITIMATE"
    else:
        result['score']="FRAUDULENT"
    
    return render(request,'form.html',result)

def about(request):
    return render(request,'inndex.html#about')


def contact(request):
    return render(request,'inndex.html#contact')




# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 13:47:55 2022

@author: Hp
"""

import pandas as pd
import numpy as np
import datetime as dt
import re 


df1 = pd.read_excel(r'C:/Users/Hp/Desktop/lufian2021.xlsx')
df2 = pd.read_excel(r'C:/Users/Hp/Desktop/lufian2021_1.xlsx')
df3 = pd.read_excel(r'C:/Users/Hp/Desktop/lufian2021_2.xlsx')

anaveri = pd.concat([df1, df2,df3], axis=0)

sontarih = dt.datetime(2021,12,31) 
#Rfm için son tarihi belirliyoruz
anaveri['tarih'] = anaveri['tarih'].astype('string') 
#İlk etapta object olarak düşen tarih datasını string veri tipine çeviriyoruz.
 
anaveri['saat'] = anaveri['saat'].astype('string')
#İlk etapta object olarak düşen saat datasını string veri tipine çeviriyoruz.

anaveri["tarih"]=anaveri["tarih"]+" "+anaveri["saat"]
#String tipine çevirilen tarih ve saat datalarını birleştiriyorz.

anaveri.tarih= anaveri.tarih.apply(pd.to_datetime)
#String tipine çevirilen tarih ve saat datalarını birleştirdikten sonra 
#tarih formatına çeviriyoruz.

anaveri['müsteri'] = anaveri['müsteri'].astype('string')
#Müşteri isimlerini stringe çeviriyoruz.

anaveri['id'] = anaveri['id'].astype('string')
#Müşteri idlerini string veri tipine çeviriyoruz

anaveri['magaza'] = anaveri['magaza'].astype('string')
#Mağaza isimlerini string veri tipine çeviriyoruz


anaveri['magaza_tipi'] = anaveri['magaza_tipi'].astype('string')
#Mağaza bilgilerini string veri tipine çeviriyoruz

anaveri["gün"]=anaveri.tarih.dt.week
#Gün bilgisini aldık

anaveri["ay"]=anaveri.tarih.dt.month
#Ay bilgisini aldık

anaveri["yıl"]= anaveri.tarih.dt.year
#Yıl bilgisini aldık.


def clean_text(text):
    text = text.lower() # Bütün karakterleri küçük harfe dönüştür
    text = text.replace("'","") # ' işaretlerini kaldır
    text = re.sub(r'\s+', ' ', text) # birden fazla boşluk var ise bunları tek boşluk ile değiştir
    text = text.strip() # text metnin başlangıç ve sonundaki boşluk (var ise) gitsin
    return text

#bazı metinler düzgün yazılmamıştır bu metinleri düzenleyeceğiz.

anaveri['müsteri'] = anaveri['müsteri'].map(clean_text)


df= anaveri[(anaveri['ciro'] >39.99) & (anaveri.magaza != 'LP E-Store')]
#Ürünlerin cirosu 39.99 tlden başlar ve iadeli satışları kaldırömış oluruz.
#LP E-Store e-ticaret satışları dahil değildir.
#Mağazacılık datalarını inceleyeceğiz.

new = df.groupby(['id', 'müsteri','magaza','magaza_tipi','tarih'])["miktar", "ciro"].apply(lambda x : x.astype(int).sum())
#Alım miktarları ve cironun toplamını yazdıracağız.

rfmTable=new.groupby(['müsteri','magaza','id','miktar']).agg({
   'tarih' : lambda x: (sontarih-x.max()).days,
   'id' : lambda x: len(x),
   'ciro': 'sum'})

#Rfm değerlerinin hesaplanması yapılıyor.
rfmTable.rename(columns = {
          'tarih' : 'recency',
          'id':'frequency',
          'ciro':'monetary'
    }, inplace=True)
#Rfm değerlerinin sütunlarını adlandırıyoruz.
##############################################################################

#2 tür aykırı değer vardır ve veri kümemizi çarpıtabileceğinden aykırı 
#değerleri ele alacağız

# 1. İstatistiksel
# 2. Etki alanına özgü değer.


#Miktar Sıklığı ve Güncelliğinin Aykırı Analizi

rfmTable.to_excel(r'C:/Users/Hp/Desktop/2020_UrunGrubu.xlsx',index=False)
rfmTable2.to_excel(r'C:/Users/Hp/Desktop/2021_UrunGrubu.xlsx',index=False)
rfmTable3.to_excel(r'C:/Users/Hp/Desktop/2022_UrunGrubu.xlsx',index=False)



---  ------              --------------   -----         
 #0   InvoiceDate         318521 non-null  datetime64[ns]
 #1   RetailCustomerCode  318521 non-null  object        
 #2   StoreDescription    318521 non-null  object        
 #3   NetQty1             318521 non-null  int64         
 #4   NetAmount           318521 non-null  float64       
 #5   FirstLastName       318521 non-null  object        
 #6   ProductAtt01Desc    318279 non-null  object        
 #7   InvoiceYear   





















































##############################################################################
quantiles = rfmTable[['recency','frequency','monetary']].quantile([.33, .66, .99]).to_dict()
quantiles

def r_score(x):
    if x <= quantiles['recency'][.33]:
        return 4
    elif x <= quantiles['recency'][.66]:
        return 3
    elif x <= quantiles['recency'][.99]:
        return 2
    else:
        return 1 
    
    
def f_score(x):
    if x == 1:
        return 1
    elif x == 2 : 
        return 2
    elif x ==3 :
        return 3
    else:
        return 4
 
def m_score(x,c):
    if x <= quantiles['recency'][.33]:
        return 1
    elif x <= quantiles['recency'][.66]:
        return 2
    elif x <= quantiles['recency'][.99]:
        return 3
    else:
        return 4 
      
rfmTable['RScore'] = rfmTable['recency'].apply(lambda x: r_score(x))
rfmTable['FScore'] = rfmTable['frequency'].apply(lambda x: f_score(x)) 
rfmTable['MScore'] = rfmTable['monetary'].apply(lambda x: m_score(x, 'monetary'))



rfmTable['RFMScore'] = rfmTable.RScore.astype(str) +  rfmTable.FScore.astype(str) +rfmTable.MScore.astype(str)











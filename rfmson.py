# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 09:06:58 2021

@author: Hp
"""

import pandas as pd
import datetime as dt
import numpy as np

# Görselleştirme için
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import plotly


# Kümelemede sayısal veriler ile işlem yapacağımızdan scaling gerekiyor.
from sklearn.preprocessing import scale

# K-Means'in çağırılması.
from sklearn.cluster import KMeans

from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import cut_tree





df =pd.read_excel(r'C:\Users\Hp\Desktop\nebimeylul.xlsx',sheet_name='Sheet1')
#iade etmeyen müşterileri aldf =pd.read_excel(r'C:\Users\Hp\Desktop\nebimeylul.xlsx',sheet_name='Sheet1')
dık.
df1 = df.loc[(df.ciro > 0)]

#iade eden müşterilerin datası
df_iade = df.loc[(df.ciro <= 0)]


#En fazla müşteriye sahip 12 mağaza

müsteri1 = df1.groupby('magazaismi')['müsteri_id'].nunique().sort_values(ascending=False).reset_index().head(11)
plt.figure(figsize=(40,8))
sns.barplot(data = müsteri1, x ='magazaismi', y = 'müsteri_id', palette='Greens_d')

plt.figure(figsize=(8,5))
sns.distplot(rfmTable.frequency, kde = False, rug=True)

##Müşterilerin tarih bazında mağazalarda kazandıkları puan
df_t=df1.groupby(['müsteri','magazaismi'])['kazanilanpuan'].sum().sort_values(ascending=False)
df_t=df_t.to_frame()
df_t

##Müşterilerin tarih bazında mağazalarda kullandıkları puan
df_f=df1.groupby(['müsteri','magazaismi'])['kullanilanpuan'].sum().sort_values(ascending=False)
df_f=df_f.to_frame()
df_f
#Rfm değişkenlerinin ana bileşenleri olan receny, frequency, monetary değişkenlerni
#müşteri bazında diğer kolonların ortalamasını alıp hesaplıyoruz.
eskitarih = df['tarih'].min()
yenitarih = df['tarih'].max()

sontarih = dt.datetime(2021,9,13)
df['Gunfarkı'] = sontarih - df['tarih']
df['Gunfarkı'].astype('timedelta64[D]')
df['Gunfarkı'] = df['Gunfarkı'] / np.timedelta64(1, 'D')

rfmTable=df.groupby(['müsteri','magazaismi']).agg({
   'tarih' : lambda x: (sontarih-x.max()).days,
   'müsteri' : 'count',
   'ciro': 'sum'})

rfmTable.rename(columns = {
          'tarih' : 'recency',
          'müsteri':'frequency',
          'ciro':'monetary'
    }, inplace=True)

rfmTable.reset_index()####
############################################################################

###STANDARİZATİON

X=rfmTable[['recency','frequency','monetary']]

from sklearn.preprocessing import StandardScaler

X_std = StandardScaler().fit_transform(X)
RFM_std = pd.DataFrame(data = X_std, columns = ['recency','frequency','monetary'])
RFM_std.describe()

######################

from sklearn.cluster import KMeans
inertia = []

for i in range(1, 11):
  kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
  kmeans.fit(RFM_std.values)
  inertia.append(kmeans.inertia_)

plt.figure(figsize=(12, 8))
plt.plot(inertia)

###############################


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
kmeans.fit(RFM_std.values)

RFM_std['cluster']= kmeans.labels_



############################################################################
quantiles = rfmTable[['recency','frequency','monetary']].quantile([.2,.4,.6,.8]).to_dict()
quantiles

def r_score(x):
    if x <= quantiles['recency'][.2]:
        return 4
    elif x <= quantiles['recency'][.4]:
        return 3
    elif x <= quantiles['recency'][.6]:
        return 2
    elif x <= quantiles['recency'][.8]:
        return 1
    else:
        return 1
def f_score(x):
    if x == 1:
        return 1
    elif x == 2  or x == 3: 
        return 2
    elif x ==4 or  x== 5:
        return 3
    elif x ==6 or x== 7:
        return 4
    else:
        return 5

    
def m_score(x,c):
    if x <= quantiles[c][.2]:
        return 1
    elif x <= quantiles[c][.4]:
        return 2
    elif x <= quantiles[c][.6]:
        return 3
    elif x <= quantiles[c][.8]:
        return 4
    else:
        return 5
    #percantiles yüzdelikler kısmı#
#Bulunan skorlar birleştirildi.

### RFM Skorlarının İstatistikleri #######

veri1 = rfm.groupby('RfmScore').agg({
'recency': ['mean','min','max','count'],
'frequency': ['mean','min','max','count'],
'monetary': ['mean','min','max','count'] }).round(1)

 #Çeyreklikler (r,m) baza alınarak  ve f  değerlerinin skorları(manuel hesaplama) bulundu.   
rfmTable['RSegment'] = rfmTable['recency'].apply(lambda x: r_score(x))
rfmTable['FSegment'] = rfmTable['frequency'].apply(lambda x: f_score(x)) 
rfmTable['MSegment'] = rfmTable['monetary'].apply(lambda x: m_score(x, 'monetary'))

#Segment Belirleme
rfmTable['RfmScore'] = rfmTable.RSegment.astype(str) +  rfmTable.FSegment.astype(str) +rfmTable.MSegment.astype(str)
segments=[]
for r,f,m in zip(rfmTable['RSegment'].to_numpy(),rfmTable['FSegment'].to_numpy(),rfmTable['MSegment'].to_numpy()):
    if(r>=4 and r<=5 ) and (f>=4 and f<=5 ) and (m >=4 and m<=5 ):
        segments.append('Şampiyon')
        
    elif(r>=2 and r<=5 ) and (f>=2 and f<=5 ) and (m >=2 and m<=5 ):
        segments.append('Sadık Müşteri')
        
    elif(r>=4 and r<=5 ) and (f==1 ) and (m >=1 and m<=5 ):
        segments.append('Yeni Müşteri')
        
    elif(r>=3 and r<=5 ) and (f>=1 and f<=3 ) and (m >=1 and m<=4 ):
        segments.append('Potansiyel Sadık')
        
    elif(r>=4 and r<=5) and (f==1 ) and (m==1 ):
        segments.append('Son müşteriler')
        
    elif(r>=3 and r<=4 ) and (f==1 ) and (m>=1 ):
        segments.append('Umut Veren Müşteriler')
          
    elif(r>=2 and r<=3 ) and (f>=2 and f<=3 ) and (m >=2 and m<=3 ):
        segments.append('İhtiyaç Duyulan Müşteriler')
        
    elif(r>=2 and r<=3 ) and (f>=1 and f<=2 ) and (m >=2 and m<=3 ):
        segments.append('Uykucu Müşteriler')
    
    elif(r>=1 and r<=2 ) and (f>=2 and f<=5 ) and (m >=2 and m<=5 ):
        segments.append('Riskli Müşteri')
    
    elif(r>=1 and r<=2 ) and (f>=1 and f<=5 ) and (m >=3 and m<=5 ):
        segments.append('Kaybedilemez Müşteri')
        
    elif(r>=1 and r<=2 ) and (f>=1 and f<=2) and (m >=1 and m<=2 ):
        segments.append('Kayıp Müşteriler')
        
    else:
        segments.append('İhtiyaç Duyulan Müşteri')
        
rfmTable['Segment'] = segments
rfm = rfmTable.reset_index()
rfm.to_excel(r'C:\Users\Hp\Desktop\rfm1.xlsx',index=False)

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 6))

for i, p in enumerate(['RSegment', 'FSegment', 'MSegment']):
    parameters = {'RSegment':'recency', 'FSegment':'frequency', 'MSegment':'monetary'}
    y = rfmTable[p].value_counts().sort_index()
    x = y.index
    ax = axes[i]
    bars = ax.bar(x, y, color='silver')
    ax.set_frame_on(False)
    ax.tick_params(left=False, labelleft=False, bottom=False)
    ax.set_title('Distribution of {}'.format(parameters[p]),
                fontsize=14)
    for bar in bars:
        value = bar.get_height()
        if value == y.max():
            bar.set_color('firebrick')
        ax.text(bar.get_x() + bar.get_width() / 2,
                value - 5,
                '{}\n({}%)'.format(int(value), int(value * 100 / y.sum())),
               ha='center',
               va='top',
               color='w')

plt.show()


fig, axes = plt.subplots(nrows=5, ncols=5,
                         sharex=False, sharey=True,
                         figsize=(10, 10))

# count the number of customers in each segment
segments_counts = rfm['Segment'].value_counts().sort_values(ascending=True)

fig, ax = plt.subplots()

bars = ax.barh(range(len(segments_counts)),
              segments_counts,
              color='silver')
ax.set_frame_on(False)
ax.tick_params(left=False,
               bottom=False,
               labelbottom=False)
ax.set_yticks(range(len(segments_counts)))
ax.set_yticklabels(segments_counts.index)

for i, bar in enumerate(bars):
        value = bar.get_width()
        if segments_counts.index[i] in ['Şampiyon', 'Sadık Müşteri']:
            bar.set_color('firebrick')
        ax.text(value,
                bar.get_y() + bar.get_height()/2,
                '{:,} ({:}%)'.format(int(value),
                                   int(value*100/segments_counts.sum())),
                va='center',
                ha='left'
               )

plt.show()




########
groups = rfmTable['Segment'].values.tolist()
harcama = rfmTable['Segment'].values.tolist()

trace = go.Pie(labels =groups ,values = harcama, hoverinfo = 'label+percent', textinfo='value', textfont = dict(size=25),
               pull=.4, hole=.2, marker = dict(line=dict(color='#000000'),width=3))

iplot([trace])    
    
    
    
    )








groups = rfmTable['Segment'].values.tolist()
harcama = rfmTable['Segment'].values.tolist()

trace = go.Pie(labels, values = harcama, hoverinfo = 'label+percent', textinfo='value', textfont = dict(size=25),
               pull=.4, hole=.2, marker = dict(line=dict(color='#000000'),width=3))

iplot([trace])








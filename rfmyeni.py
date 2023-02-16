# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 10:46:42 2022

@author: Hp
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt



import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import plotly

#verisetimizi hazır hale getiriyoruz.

d =pd.read_excel(r'C:\Users\Hp\Desktop\migration.xlsx',sheet_name='Sheet1')
d1 =pd.read_excel(r'C:\Users\Hp\Desktop\migration.xlsx',sheet_name='Sheet2')

dd1 = pd.concat([d, d1], axis=0)

dd1.to_excel(r'C:\Users\Hp\Desktop\migration1.xlsx',index=False)

df =pd.read_excel(r'C:\Users\Hp\Desktop\migration1.xlsx',sheet_name='Sheet1')

df['tarih'] = pd.to_datetime(df['tarih'], format = "%d-%m-%Y %H:%M")


eskitarih = df['tarih'].min()
yenitarih = df['tarih'].max()

sontarih = dt.datetime(2021,9,30)
df['Gunfarkı'] = sontarih - df['tarih']
df['Gunfarkı'].astype('timedelta64[D]')
df['Gunfarkı'] = df['Gunfarkı'] / np.timedelta64(1, 'D')


rfmTable=df.groupby(['müsteri','ceptelefonu']).agg({
   'tarih' : lambda x: (sontarih-x.max()).days,
   'ceptelefonu' : 'count',
   'ciro': 'sum'})

rfmTable.rename(columns = {
          'tarih' : 'recency',
          'ceptelefonu':'frequency',
          'ciro':'monetary'
    }, inplace=True)

rfm = rfmTable.reset_index()

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
      
rfm['RScore'] = rfm['recency'].apply(lambda x: r_score(x))
rfm['FScore'] = rfm['frequency'].apply(lambda x: f_score(x)) 
rfm['MScore'] = rfm['monetary'].apply(lambda x: m_score(x, 'monetary'))


rfm['RFMScore'] = rfm.RScore.astype(str) +  rfm.FScore.astype(str) +rfm.MScore.astype(str)

def segment(x):
    if x == '114':
        return 'Churn'
    elif x in ['313', '314', '214','213']:
        return 'Silver'
    elif x in ['324', '224']:
        return 'Gold'
    elif x in ['414', '413']:
        return 'New Customers'
    else:
        return 'Platinium'

rfm['Segments'] = rfm['RFMScore'].apply(segment)

rfm.to_excel(r'C:/Users/Hp/Desktop/Temmuz-Agustos2021.xlsx',index=False)


# Veri Görselleştirme

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 6))

for i, p in enumerate(['RScore', 'FScore', 'MScore']):
    parameters = {'RScore':'recency', 'FScore':'frequency', 'MScore':'monetary'}
    y = rfm[p].value_counts().sort_index()
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
segments_counts = rfm['Segments'].value_counts().sort_values(ascending=True)

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
        if segments_counts.index[i] in ['Platinium', 'Gold']:
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


###############################################################################
marmara = ["İstanbul", "Balikesir", "Bursa", "Tekirdağ", "Çanakkale",
          "Yalova", "Kocaeli", "Kırklareli", "Edirne", "Bilecik", "Sakarya", "Balıkesir"]
for i in marmara:
    df.loc[df["il"] == i, "Bolge"] = "Marmara"
###############################################################################
ege = ["İzmir", "Manisa", "Aydın", "Denizli", "Uşak", "Afyonkarahisar", "Kütahya", "Muğla"]
for i in ege:
    df.loc[df["il"] == i, "Bolge"] = "Ege"
###############################################################################
ic_anadolu = ["Ankara", "Konya", "Kayseri", "Eskişehir", "Sivas", "Kırıkkale", "Aksaray",
             "Karaman", "Kırşehir", "Niğde", "Nevşehir", "Yozgat", "Çankırı"]
for i in ic_anadolu:
    df.loc[df["il"] == i, "Bolge"] = "İç Anadolu"
##############################################################################
karadeniz = ["Amasya", "Artvin", "Bartın", "Bayburt", "Bolu", "Çorum", "Gümüşhane", "Giresun",
            "Karabük", "Kastamonu", "Ordu", "Rize", "Samsun", "Sinop", "Tokat", "Trabzon", "Zonguldak","Düzce"]
for i in karadeniz:
    df.loc[df["il"] == i, "Bolge"] = "Karadeniz"
#################################################################################
dogu_anadolu = ["Ağrı", "Ardahan", "Bitlis", "Bingöl", "Elazığ", "Erzincan", "Erzurum",
               "Hakkari", "Iğdır", "Kars", "Malatya", "Muş","Tunceli", "Van"]
for i in dogu_anadolu:
    df.loc[df["il"] == i, "Bolge"] = "Doğu Anadolu"
#################################################################################
gdogu_anadolu = ["Gaziantep", "Diyarbakır", "Şanlıurfa", "Batman", "Adıyaman",
                "Siirt", "Mardin", "Kilis", "Şırnak"]
for i in gdogu_anadolu:
    df.loc[df["il"] == i, "Bolge"] = "Güneydoğu Anadolu"  
##################################################################################
akdeniz = ["Antalya", "Adana", "Mersin", "Hatay", "Burdur", "Osmaniye",
          "Kahramanmaraş", "Isparta"]

for i in akdeniz:
    df.loc[df["il"] == i, "Bolge"] = "Akdeniz"
    
    
df["tarih"] = df["tarih"].dt.date
    
   
    
   
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import plotly

fig = px.bar(df, x="Bolge", y="ciro", color="il", title="Completed 1st dose of Vaccine as of June 26")
fig.show()  
    
    
    
    
    
    
    
    
    
    
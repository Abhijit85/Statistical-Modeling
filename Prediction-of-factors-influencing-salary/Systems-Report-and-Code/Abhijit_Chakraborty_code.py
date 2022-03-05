import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
fontsize2use = 10
fontprop = fm.FontProperties(size=fontsize2use)
plt.rcParams['font.size'] = '16'

features = ["age","workclass","fnlwgt","education","education-num","marital-status","occupation","relationship","race","gender","capital-gain","capital-loss","hours-per-week","native-country","income"]

data = pd.read_csv("dataset/adult.data.txt" , delimiter=",\s" , names = features , engine = 'python')

# importing data

path = "dataset/adult.data.txt"
df = pd.read_csv(path, header=None)

column_dict = {
        0:"age", 1:"workclass", 2:"fnlwgt", 3:"education", 4:"education-num", 5:"marital-status",
        6:"occupation", 7:"relationship", 8:"race", 9:"sex", 10:"capital-gain", 11:"capital-loss",
        12:"hours-per-week", 13:"native-country", 14:">50K"
        }

df = df.rename(columns=column_dict)


#Mosaic
from statsmodels.graphics.mosaicplot import mosaic
temp = data[['relationship','income']].copy()
# temp = temp.loc[temp['marital-status'] != 'Married-AF-spouse']
plt.rcParams['font.size'] = 10
# plt.figure(figsize=(10,10))
# plt.rcParams['font.size'] = 10
fig,dic = mosaic(temp,['relationship','income'],labelizer=lambda x: '',axes_label=True,gap=0.02,label_rotation=90)
# plt.xticks([0,1],labels=['No Loss','Loss'])
plt.yticks([0,1],labels=['Less than 50K','Greater than 50K'])
plt.title('Relationship and income')

#Pie
np.seterr(divide='ignore', invalid='ignore')
status = set(data['relationship'].unique())
ratios = [0]*len(status)
for i,s in enumerate(status):
    print(s)
    ratios[i] = np.sum((temp['relationship']==s) & (temp['income']==0))
plt.figure(figsize=(10,10))
plt.rcParams['font.size'] = 18
ratios = np.array(ratios)/np.sum(ratios)
status_arr = np.array(list(status))
print(ratios,status_arr)
status_arr[ratios<=0.02] = 'other'
# ratios[ratios< 0.02] = 0
plt.pie(list(ratios[status_arr!='other'])+[np.sum(ratios[status_arr=='other'])],labels=list(status_arr[status_arr!='other'])+['other'], autopct='%1.1f%%',)
# plt.pie(,labels=['other'], autopct='%1.1f%%',)
plt.title('Relationship for <50K income croup')
plt.show()

#%% md

## Gender

#%%

# Data manipulation

df_sex = df[['sex', 'age']].groupby(['sex']).count()
df_sex = df_sex.rename(columns={"age": "Count"})

mask_female = df['sex'] == " Female"
mask_male = df['sex'] == " Male"

df_female = df[mask_female][['age', '>50K']].groupby(['>50K'], as_index = False).count()

df_male = df[mask_male][['age', '>50K']].groupby(['>50K'], as_index = False).count()
plt.figure(figsize=(12,7))

explode = (0.2, 0)
color_list = plt.cm.tab20c(np.linspace(0, 2, 10))
plt.pie(df_female['age'],
        labels=df_female['>50K'],
        shadow=False,
        colors=color_list,
        explode=explode,
        autopct='%1.1f%%', textprops={'fontsize': 14}
       )
plt.axis('equal')
plt.title("Females with Salary above 50K\n", fontsize=22)

plt.show()

#%%

plt.figure(figsize=(12,7))

explode = (0.2, 0)
color_list = plt.cm.tab20c(np.linspace(0, 2, 10))
plt.pie(df_male['age'],
        labels=df_male['>50K'],
        shadow=False,
        colors=color_list,
        explode=explode,
        autopct='%1.1f%%', textprops={'fontsize': 14}
       )
plt.axis('equal')
plt.title("Males with Salary above 50K\n", fontsize=22)

plt.show()
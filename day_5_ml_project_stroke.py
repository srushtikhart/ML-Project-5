# -*- coding: utf-8 -*-
"""Day 5 ML Project Stroke.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZYDFFdQN1gByKnaOwwzXAVEkOl_xND1v
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/content/drive/MyDrive/stroke.csv')
df.head()

df.describe()

df.shape

df.isnull().sum()

bmi_mean = df['bmi'].mean()
df['bmi'].fillna(value=bmi_mean, inplace=True)
bmi_mean

df.isnull().sum()

df.drop(['id'], axis=1, inplace=True)

df.head()

plt.figure(figsize=(12,6))
sns.distplot(df['age'],bins=15)
plt.show()

plt.figure(figsize=(12,6))
sns.distplot(df[df['stroke'] == 0]["age"], color='green', label='No Stroke')
sns.distplot(df[df['stroke'] == 1]["age"], color='red', label='Stroke')

plt.title('No stroke vs stroke by age', fontsize=15)
plt.xlim([18,100])
plt.show()

sns.countplot(x='gender', data=df, hue='stroke')

df['gender'].value_counts()

df.drop(df[df['gender'] == 'Other'].index, inplace=True)

sns.countplot(x='gender', data=df, hue='stroke')

sns.countplot(x='stroke', data=df)
df.stroke.value_counts()

"""hugely class imbalance"""

sns.countplot(x='smoking_status', data=df);

x =df.iloc[:,0:-1].values
y =df.iloc[:,-1].values

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

l_e = LabelEncoder()
x[:,4] = l_e.fit_transform(x[:,4])
x[:,5] = l_e.fit_transform(x[:,5])
x[:,6] = l_e.fit_transform(x[:,6])

c_t = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [5,9])], remainder='passthrough')
x = np.array(c_t.fit_transform(x))

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

x_train.shape, y_train.shape, x_test.shape, y_test.shape

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.fit_transform(x_test)

"""unsampling the data"""

print (sum(y_train == 0))
print (sum(y_train == 1))

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
x_train, y_train = smote.fit_resample(x_train, y_train)

print (x_train.shape)
print (y_train.shape)
print (sum(y_train == 0))
print (sum(y_train == 1))

from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, confusionMatrixDisplay, precision_score, recall_score, f1_score, classification_report, roc_curve, plot_roc_curve, auc, precision_recall_curve, plot_precision_recall_curve, average_precision_score
from sklearn.model_selection import cross_val_score

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
score = cross_val_score(model, x_train, y_train, cv=5)
precision = precision_score(y_test, y_pred)
roc = roc_auc_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print(score,mean(), '%')
print(precision)
print(roc)
print(recall)
print(cm)
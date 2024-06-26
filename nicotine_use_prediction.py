# -*- coding: utf-8 -*-
"""nicotine-use-prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14JzwJFZcqt4tWp4KST3EOQ2o0tdGoX9u
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from scipy.stats import randint

df = pd.read_csv('drug_consumption.csv')
print(df.columns)
df.head()

def replace_clx(value):
  if value.startswith('CL'):
    return int(value[2:])
  else:
    return value
df['Nicotine'] = df['Nicotine'].apply(replace_clx)
df['Alcohol'] = df['Alcohol'].apply(replace_clx)

fig, axs = plt.subplots(1, 2, figsize=(13, 5))
axs[0].hist(df['Nicotine'], bins=10, edgecolor='k', alpha=0.7, label='Nicotine Usage')
axs[0].set_title('Nicotine Usage')

axs[1].hist(df['Alcohol'], bins=10, edgecolor='k', alpha=0.7, label='Alcohol Usage', color='lightcoral')
axs[1].set_title('Alcohol Usage')

plt.show()

def replace_s(value):
  if value <= 2:
    return 0
  else:
    return 1
df['Nicotine'] = df['Nicotine'].apply(replace_s)

features = ['Age', 'Gender', 'Education', 'Country', 'Ethnicity', 'Nscore',
            'Escore', 'Oscore', 'Ascore', 'Cscore', 'Impulsive', 'SS', 'Alcohol']
X = df[features]
y = df['Nicotine']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
print(f'X_train shape: {X_train.shape}\nX_test shape: {X_test.shape}')

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

param_dist = {'n_estimators': randint(50,500),
              'max_depth': randint(1,30)}

rf2 = RandomForestClassifier()

rand_search = RandomizedSearchCV(rf2,
                                 param_distributions = param_dist,
                                 n_iter=7)
rand_search.fit(X_train, y_train)

best_rf = rand_search.best_estimator_

y_pred2 = best_rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred2)
precision = precision_score(y_test, y_pred2)
recall = recall_score(y_test, y_pred2)
print(f'Accuracy: {accuracy}\nPrecision: {precision}\nRecall: {recall}')

cm = confusion_matrix(y_test, y_pred2)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

feature_importances = pd.Series(best_rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
feature_importances.plot.bar();
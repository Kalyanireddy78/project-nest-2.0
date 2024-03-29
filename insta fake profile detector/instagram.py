# -*- coding: utf-8 -*-
"""instagram

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vouKXOqWEBpuCwJw3Fl4IIsKqufSQNPd
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Load the data
df = pd.read_csv('instagram.csv')

# Explore the data
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())

# Visualize the data
sns.set(style="whitegrid")

# List of features
features = ['profile pic', 'nums/length username', 'fullname words', 'nums/length fullname', 'name==username',
            'description length', 'external URL', 'private', '#posts', '#followers', '#follows']

# Plot histograms for each feature
plt.figure(figsize=(20,15))
for i, feature in enumerate(features):
    plt.subplot(4, 4, i+1)
    sns.histplot(df[feature], kde=False, bins=10)
plt.tight_layout()
plt.show()

# Split the data into features and target
X = df.drop('fake', axis=1)
y = df['fake']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=['Actual Real', 'Actual Fake'], columns=['Predicted Real', 'Predicted Fake'])
plt.figure(figsize=(6, 4))
sns.heatmap(cm_df, annot=True, fmt='g', cmap='Blues')
plt.title('Confusion Matrix')
plt.show()

# Define preprocessing function
def preprocess_data_X1(profile_pic, nums_length_username, fullname_words, name_username, description_length, external_URL, private):
    data = [profile_pic, nums_length_username, fullname_words, name_username, description_length, external_URL, private]
    processed_data = np.array([data[:-1]])  # Exclude nums/length fullname
    return processed_data

# Save the model and scaler
import pickle
with open('instagram_model.pkl', 'wb') as file:
    pickle.dump(model, file)

with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

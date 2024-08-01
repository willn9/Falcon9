# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
print(df.head(10))
print(df.tail())

# df.describe(include="all")

print(df.isnull().sum() / len(df) * 100)

print(df.dtypes)

print(df[['LaunchSite']].value_counts())

# Apply value_counts() on column LaunchSite
print(df[['LaunchSite']].value_counts())

# Apply value_counts on Orbit column
print(df[['Orbit']].value_counts())

# landing_outcomes = values on Outcome column
landing_outcomes = df['Outcome']
print(landing_outcomes)

for i, outcome in enumerate(landing_outcomes.unique()):
    print(i, outcome)

# Define the set of bad outcomes
bad_outcomes = {'False ASDS', 'False Ocean', 'False RTLS', 'None ASDS', 'None None'}

# Create the landing_class list
landing_class = [0 if outcome in bad_outcomes else 1 for outcome in df['Outcome']]

df['Class'] = landing_class
print(df[['Class']].head(8))

print(df['Class'].mean())

df.to_csv("dataset_part_2.csv", index=False)
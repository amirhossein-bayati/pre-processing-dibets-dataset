# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from fitter import Fitter, get_common_distributions


# Read File Function
def read_file(name):
    data = pd.read_excel(name)
    return data


# Write And Save New Data On Excel
def re_write_file(data):
    data.to_excel('new-release.xlsx')


# Read File And Save On Data
data = read_file("pima-indians-diabetes.v1.xlsx")


# Delete Empty Records
data.dropna(inplace=True)


# Remove Wrong Formats
for i in data.index:
    try:
        data.loc[i] = pd.to_numeric(data.loc[i])
    except:
        data.drop(i, inplace=True)


# Remove Duplicated Items
data.drop_duplicates(inplace=True)

re_write_file(data)
data = read_file("new-release.xlsx")
data.pop('Unnamed: 0')


# Remove Outlier Data
for col in data:
    Q1 = data[col].describe()[4]
    Q3 = data[col].describe()[6]
    IQR = data[col].describe()[5]
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    for row in data.index:
        item = data.loc[row, col]
        if item < lower or item > upper:
            data.drop(row, inplace=True)


# Remove Wrong Data on output
for x in data.index:
    if data.loc[x, "output"] > 1 or data.loc[x, "output"] < 0:
        data.drop(x, inplace=True)

    if data.loc[x, "A4"] == 0 or data.loc[x, "A2"] == 0 or data.loc[x, "A3"] == 0 or data.loc[x, "A5"] == 0:
        data.drop(x, inplace=True)

# Reset Data Index
data = data.reset_index(drop=True)


# Calculate Mathematical Operations
res = []
for column in data:
    row = {
        "minimum": data[column].min(),
        "maximum": data[column].max(),
        "median": data[column].median(),
        "average": data[column].mean(),
        "standard-deviation": data[column].std(),
        "variance": data[column].var()
    }
    res.append(row)

resDf = pd.DataFrame(res, index=[col for col in data])


# Draw Distribution
for col in data:
    f = Fitter(data[col], distributions=get_common_distributions())
    f.fit()
    f.summary()
    plt.show()
    plt.clf()


# Draw Histogram
for column in data:
    plt.hist(data[column], rwidth=0.9)
    plt.xlabel(column)
    plt.ylabel("count")
    plt.show()


# Normalize Data
normalized_df = (data-data.min())/(data.max()-data.min())
res = []
for column in normalized_df:
    row = {
        "minimum": normalized_df[column].min(),
        "maximum": normalized_df[column].max(),
        "median": normalized_df[column].median(),
        "average": normalized_df[column].mean(),
        "standard-deviation": normalized_df[column].std(),
        "variance": normalized_df[column].var()
    }
    res.append(row)

normalized_result = pd.DataFrame(res, index=[col for col in data])


# Draw Convolution
sn.heatmap(data.corr(), annot=True, fmt=".2f", cmap="Blues")
plt.show()


# Draw Scatter Plot
plt.clf()
sn.scatterplot(data=data, x="A1", y="A8", hue="output")
plt.show()

plt.clf()
sn.scatterplot(data=data, x="A2", y="A5", hue="output")
plt.show()

plt.clf()
sn.scatterplot(data=data, x="A4", y="A6", hue="output")
plt.show()

plt.clf()
sn.scatterplot(data=data, x="A3", y="A8", hue="output")
plt.show()

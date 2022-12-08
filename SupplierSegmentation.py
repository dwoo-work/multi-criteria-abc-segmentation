# SUPPLIER SEGMENTATION
#------------------------------------------------------------------------------------------
# PART 1 - PREPARATION

# Import the required libraries.

import pandas as pd
import inventorize as inv
import seaborn as sns

# Import and clean the CSV dataframe.

supplier = pd.read_csv('supplier_data_sample_utf8.csv')

supplier = supplier.drop_duplicates()
supplier = supplier.dropna()

supplier.info()
supplier.head()

# For each of the four risk factors, convert N or Y, to its numerical representative (refer to the legend in README.md).

# Convert availability section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present)
# Then, add all responsed values from Q1 to Q5, to a consolidated availability column within the dataframe.

supplier['AVAILABILITY_Q1'] = pd.to_numeric(supplier['AVAILABILITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q2'] = pd.to_numeric(supplier['AVAILABILITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q3'] = pd.to_numeric(supplier['AVAILABILITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q4'] = pd.to_numeric(supplier['AVAILABILITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q5'] = pd.to_numeric(supplier['AVAILABILITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['AVAILABILITY'] = supplier['AVAILABILITY_Q1'] + supplier['AVAILABILITY_Q2'] + supplier['AVAILABILITY_Q3'] + supplier['AVAILABILITY_Q4'] + supplier['AVAILABILITY_Q5']

# Convert suppliers section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present)
# Then, add all responsed values from Q1 to Q5, to a consolidated suppliers column within the dataframe.

supplier['SUPPLIERS_Q1'] = pd.to_numeric(supplier['SUPPLIERS_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q2'] = pd.to_numeric(supplier['SUPPLIERS_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q3'] = pd.to_numeric(supplier['SUPPLIERS_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q4'] = pd.to_numeric(supplier['SUPPLIERS_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q5'] = pd.to_numeric(supplier['SUPPLIERS_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['SUPPLIERS'] = supplier['SUPPLIERS_Q1'] + supplier['SUPPLIERS_Q2'] + supplier['SUPPLIERS_Q3'] + supplier['SUPPLIERS_Q4'] + supplier['SUPPLIERS_Q5']

# Convert product complexity section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present)
# Then, add all responsed values from Q1 to Q5, to a consolidated product complexity column within the dataframe.

supplier['PRODUCT_COMPLEXITY_Q1'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q2'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q3'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q4'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q5'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['PRODUCT_COMPLEXITY'] = supplier['PRODUCT_COMPLEXITY_Q1'] + supplier['PRODUCT_COMPLEXITY_Q2'] + supplier['PRODUCT_COMPLEXITY_Q3'] + supplier['PRODUCT_COMPLEXITY_Q4'] + supplier['PRODUCT_COMPLEXITY_Q5']

# Convert product complexity section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present)
# Then, add all responsed values from Q1 to Q5, to a consolidated product complexity column within the dataframe.

supplier['PRICE_STABILITY_Q1'] = pd.to_numeric(supplier['PRICE_STABILITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q2'] = pd.to_numeric(supplier['PRICE_STABILITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q3'] = pd.to_numeric(supplier['PRICE_STABILITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q4'] = pd.to_numeric(supplier['PRICE_STABILITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q5'] = pd.to_numeric(supplier['PRICE_STABILITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['PRICE_STABILITY'] = supplier['PRICE_STABILITY_Q1'] + supplier['PRICE_STABILITY_Q2'] + supplier['PRICE_STABILITY_Q3'] + supplier['PRICE_STABILITY_Q4'] + supplier['PRICE_STABILITY_Q5']

# Create new variable(s) within the CSV dataframe.

supplier['risk_index'] = supplier['AVAILABILITY'] + supplier['SUPPLIERS'] + supplier['PRODUCT_COMPLEXITY'] + supplier['PRICE_STABILITY']

# Evaluate value index, and add its column into the supplier dataframe.
# Low value index: Value is below the median.
# High value index: Value is above the median.

supplier['value'] = supplier['PRICEEACH'] * supplier['QUANTITYORDERED']
supplier.value.describe()

# Create a new CSV dataframe (cleaned data).

supplier_clean = supplier.copy()
supplier_clean.info()

#------------------------------------------------------------------------------------------
# PART 2 - PERFORM SUPPLIER SEGMENTATION USING KRALJIC'S MATRIX

# Create a function that defines each supplier in one of the four Kraljic's Matrix quadrants.

def category (x,y):
    if ((x >= supplier_clean.value.median()) & (y >= 1)):
        return 'strategic'
    if ((x >= supplier_clean.value.median()) & (y < 1)):
        return 'leverage'
    if ((x < supplier_clean.value.median()) & (y < 1)):
        return 'non-critical'
    if ((x < supplier_clean.value.median()) & (y >= 1)):
        return 'bottleneck'

for i in range (supplier_clean.shape[0]):
    supplier_clean.loc[i,'category'] = category(supplier_clean.loc[i,'value'],
                                                supplier_clean.loc[i,'risk_index'])

supplier_clean['risk_index'].value_counts()
supplier_clean.category.value_counts()

# Create a scatter plot for all the suppliers, with different colors for each Kraljic's Matrix quadrants.

kraljic_diagram = sns.scatterplot(x = 'risk_index', y = 'value', data = supplier_clean, hue= 'category')
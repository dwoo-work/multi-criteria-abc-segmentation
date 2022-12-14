# SUPPLIER SEGMENTATION
#------------------------------------------------------------------------------------------
# PART 1 - PREPARATION

import pandas as pd
import seaborn as sns

supplier = pd.read_csv('https://raw.githubusercontent.com/dwoo-work/multi-criteria-abc-segmentation/main/src/supplier_data_sample_utf8.csv')
supplier = supplier.drop_duplicates()
supplier = supplier.dropna()
supplier.info()
supplier.head()

supplier['AVAILABILITY_Q1'] = pd.to_numeric(supplier['AVAILABILITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q2'] = pd.to_numeric(supplier['AVAILABILITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q3'] = pd.to_numeric(supplier['AVAILABILITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q4'] = pd.to_numeric(supplier['AVAILABILITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q5'] = pd.to_numeric(supplier['AVAILABILITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['AVAILABILITY'] = supplier['AVAILABILITY_Q1'] + supplier['AVAILABILITY_Q2'] + supplier['AVAILABILITY_Q3'] + supplier['AVAILABILITY_Q4'] + supplier['AVAILABILITY_Q5']

supplier['SUPPLIERS_Q1'] = pd.to_numeric(supplier['SUPPLIERS_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q2'] = pd.to_numeric(supplier['SUPPLIERS_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q3'] = pd.to_numeric(supplier['SUPPLIERS_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q4'] = pd.to_numeric(supplier['SUPPLIERS_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q5'] = pd.to_numeric(supplier['SUPPLIERS_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['SUPPLIERS'] = supplier['SUPPLIERS_Q1'] + supplier['SUPPLIERS_Q2'] + supplier['SUPPLIERS_Q3'] + supplier['SUPPLIERS_Q4'] + supplier['SUPPLIERS_Q5']

supplier['PRODUCT_COMPLEXITY_Q1'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q2'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q3'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q4'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q5'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['PRODUCT_COMPLEXITY'] = supplier['PRODUCT_COMPLEXITY_Q1'] + supplier['PRODUCT_COMPLEXITY_Q2'] + supplier['PRODUCT_COMPLEXITY_Q3'] + supplier['PRODUCT_COMPLEXITY_Q4'] + supplier['PRODUCT_COMPLEXITY_Q5']

supplier['PRICE_STABILITY_Q1'] = pd.to_numeric(supplier['PRICE_STABILITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q2'] = pd.to_numeric(supplier['PRICE_STABILITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q3'] = pd.to_numeric(supplier['PRICE_STABILITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q4'] = pd.to_numeric(supplier['PRICE_STABILITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q5'] = pd.to_numeric(supplier['PRICE_STABILITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['PRICE_STABILITY'] = supplier['PRICE_STABILITY_Q1'] + supplier['PRICE_STABILITY_Q2'] + supplier['PRICE_STABILITY_Q3'] + supplier['PRICE_STABILITY_Q4'] + supplier['PRICE_STABILITY_Q5']

supplier['risk_index'] = supplier['AVAILABILITY'] + supplier['SUPPLIERS'] + supplier['PRODUCT_COMPLEXITY'] + supplier['PRICE_STABILITY']

supplier['value'] = supplier['PRICEEACH'] * supplier['QUANTITYORDERED']
supplier.value.describe()

supplier_clean = supplier.copy()
supplier_clean.info()

#------------------------------------------------------------------------------------------
# PART 2 - PERFORM SUPPLIER SEGMENTATION USING KRALJIC'S MATRIX

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

kraljic_diagram = sns.scatterplot(x = 'risk_index', y = 'value', data = supplier_clean, hue= 'category').set(title = 'Suppliers Classification using the Kraljic Matrix')
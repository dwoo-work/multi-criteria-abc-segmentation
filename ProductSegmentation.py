# PRODUCT SEGMENTATION
#------------------------------------------------------------------------------------------
# PART 1 - PREPARATION

import pandas as pd
import numpy as np
import seaborn as sns
import inventorize as inv

sales = pd.read_csv('https://raw.githubusercontent.com/dwoo-work/MultiCriteriaABC.Analysis/main/src/sales_data_sample_utf8.csv')
sales = sales.drop_duplicates()
sales.info()

sales_clean = sales.copy()
sales_clean.info()

grouped = sales_clean.groupby('PRODUCTCODE').agg(total_sales = ('QUANTITYORDERED',np.sum), total_revenue = ('SALES', np.sum)).reset_index()
grouped.info()

by_store = sales_clean.groupby(['COUNTRY','PRODUCTCODE']).agg(total_sales = ('QUANTITYORDERED',np.sum), total_revenue = ('SALES',np.sum)).reset_index()
by_store.info()

#------------------------------------------------------------------------------------------
# PART 2 - ABC Analysis

abc = inv.ABC(grouped[['PRODUCTCODE', 'total_sales']])
abc.info()
abc.Category.value_counts()

sns.countplot(x = 'Category', data = abc).set(title = 'No. of A, B, and C Cat. Items for All Countries')
sns.barplot(x = 'Category', y = 'total_sales', data = abc).set(title = 'Avg. Value of A, B, and C Cat. Items for All Countries')

#------------------------------------------------------------------------------------------
# PART 3 - Multi-Criteria ABC Analysis

mc_abc = inv.productmix(grouped['PRODUCTCODE'], grouped['total_sales'], grouped['total_revenue'])
mc_abc.info()
mc_abc.product_mix.value_counts()

sns.countplot(x = 'product_mix', data = mc_abc).set(title = 'No. of A_A to C_C Cat. Items for All Countries')
sns.barplot(x = 'product_mix', y = 'sales', data = mc_abc).set(title = 'Avg. Value of A_A to C_C Cat. Items for All Countries')
sns.barplot(x = 'product_mix', y = 'revenue', data = mc_abc).set(title = 'Total Revenue of A_A to C_C Cat. Items for All Countries')

#------------------------------------------------------------------------------------------
# PART 4 - Multi-Criteria ABC Analysis on a Store Level (Australia)

mix_country = inv.productmix_storelevel(by_store['PRODUCTCODE'], by_store['total_sales'], by_store['total_revenue'], by_store['COUNTRY'])
mix_country.info()

product_mix = mix_country.groupby(['storeofsku','product_mix']).count().reset_index().iloc[:,0:3]
product_mix.info()

australia = product_mix[product_mix.storeofsku == 'Australia']
australia.info()

sns.barplot(x = 'product_mix', y = 'sku', data = australia).set(title = 'No. of A_A to C_C Cat. Items for Australia')
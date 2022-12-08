# PRODUCT SEGMENTATION
#------------------------------------------------------------------------------------------
# PART 1 - PREPARATION

# Import the required libraries.

import pandas as pd
import numpy as np
import seaborn as sns
import inventorize as inv

# Import and clean the CSV dataframe.

sales = pd.read_csv('sales_data_sample_utf8.csv')
sales = sales.drop_duplicates()
sales.info()

# Create a new CSV dataframe (cleaned data).

sales_clean = sales.copy()
sales_clean.info()

# Create a new CSV dataframe (pre-ABC data).
# This is used for both ABC Analysis and Multi-Criteria Analysis.

grouped = sales_clean.groupby('PRODUCTCODE').agg(total_sales = ('QUANTITYORDERED',np.sum), total_revenue = ('SALES', np.sum)).reset_index()
grouped.info()

# This is used for Multi-Criteria Analysis on a Store-level. For this, classification of Store is Country.

by_store = sales_clean.groupby(['COUNTRY','PRODUCTCODE']).agg(total_sales = ('QUANTITYORDERED',np.sum), total_revenue = ('SALES',np.sum)).reset_index()
by_store.info()

#------------------------------------------------------------------------------------------
# PART 2 - ABC Analysis

# Perform ABC Analysis on CSV dataframe (pre-ABC data)

abc = inv.ABC(grouped[['PRODUCTCODE', 'total_sales']])
abc.info()

abc.Category.value_counts()

# Plot the charts for ABC Analysis using Seaborn.

sns.countplot(x = 'Category', data = abc)
sns.barplot(x = 'Category', y = 'total_sales', data = abc)

#------------------------------------------------------------------------------------------
# PART 3 - Multi-Criteria ABC Analysis

# Perform Multi-Criteria ABC Analysis on CSV dataframe (pre-ABC data)

mc_abc = inv.productmix(grouped['PRODUCTCODE'], grouped['total_sales'], grouped['total_revenue'])
mc_abc.info()

mc_abc.product_mix.value_counts()

# Plot the charts for Multi-Criteria ABC Analysis using Seaborn.

sns.countplot(x = 'product_mix', data = mc_abc)
sns.barplot(x = 'product_mix', y = 'sales', data = mc_abc)
sns.barplot(x = 'product_mix', y = 'revenue', data = mc_abc)

#------------------------------------------------------------------------------------------
# PART 4 - Multi-Criteria ABC Analysis on a Store Level

# Perform Multi-Criteria ABC Analysis on Store-level on CSV dataframe (pre-ABC data)

mix_country = inv.productmix_storelevel(by_store['PRODUCTCODE'], by_store['total_sales'], by_store['total_revenue'], by_store['COUNTRY'])
mix_country.info()

product_mix = mix_country.groupby(['storeofsku','product_mix']).count().reset_index().iloc[:,0:3]
product_mix.info()

# Create a variable for Australia's product mix for analysis.

australia = product_mix[product_mix.storeofsku == 'Australia']
australia.info()

# Plot the charts for Australia's Multi-Criteria ABC Analysis using Seaborn.

sns.barplot(x = 'product_mix', y = 'sku', data = australia)
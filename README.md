# ABC Analysis

This will demonstrate to you how to perform Multi-Criteria ABC Analysis using Python.

In your sales data, you will have data for customers, products, and suppliers. However, as there are too many Stock-Keeping-Units (or SKUs), you cannot observe them individually.

Therefore, you have to group these SKUs into individual groups. From there, create and execute supply chain strategies for each of the different group.

ABC Analysis is important to the different aspects of supply chain:

- Assortment planning
- Warehouse management
- Markdowns
- Service levels
- Product rationalisation
- Supplier rationalisation
- Customer strategies

Normally, with ABC Analysis, we will classify these SKUs into either one of the three categories:

- A: Products / Suppliers / Customers that represent 80% of the business.
- B: Products / Suppliers / Customers that represent 15% of the business.
- C: Products / Suppliers / Customers that represent 5% of the business.

Once the SKUs are classified, the strategies for inventory management will be different across them:

- A: Set a higher service level for them and manage dynamically.
- B: Set a lower service level for them and manage dynamically.
- C: Don't spend much time managing and keep them as minimal as possible.

This will be all it takes, if you are performing a normal ABC Analysis using one criteria (i.e. revenue). However, if you nare looking to use two or more criterias (i.e. both quantity and revenue), then you would have to perform a Multi-Criteria ABC Analysis.

| Quantity | Revenue | Category                   |
| ---------| ------- | -------------------------- |
| A        | A       | Margin & Volume Drivers    |
| A        | B       | Volume Drivers             |
| A        | C       | Volume Drivers             |
| B        | A       | Margin Driver              |
| B        | B       | Regular                    |
| B        | C       | Regular                    |
| C        | A       | Margin Driver              |
| C        | B       | Regular                    |
| C        | C       | Slow Moving                |

By classifying SKUs using Multi-Criteria ABC Analysis, you can create a more customised and specific set of strategies.

In total, there will be three sets of scripts which make use of ABC Analysis to perform segmentation:

- Product Segmentation
- Customer Segmentation (WIP)
- Supplier Segmentation (WIP)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install:

- pandas: to perform data administration by pulling in .csv or .xlsx files.
- numpy: to perform data manipulation by establishing arrays.
- seaborn: to perform data visualisation based on matplotlib.
- inventorize: to calculate for inventory metrics, stock-out, and ABC analysis.

```bash
pip install pandas
pip install numpy
pip install seaborn
pip install inventorize
```

## Sample Dataset

You can download the sales_data_sample_utf8.csv file from the source folder, which is located [here](https://github.com/dwoo-work/Linear_Regression_Analysis_using_Python/tree/main/src).

Ensure that the file is in CSV UTF-8 format, to avoid UnicodeDecodeError later on.

## Code Explanation (for Product Segmentation)

### Part 1 - Preparation

Lines 5-8:  
Import the required libraries.
```python   
import pandas as pd
import numpy as np
import seaborn as sns
import inventorize as inv
```

Lines 10-12:  
Import and clean the CSV dataframe.
```python   
sales = pd.read_csv('sales_data_sample_utf8.csv')
sales = sales.drop_duplicates()
sales.info()
```

Lines 14-15:  
Create a new CSV dataframe (cleaned data).
```python   
sales_clean = sales.copy()
sales_clean.info()
```

Lines 17-18:  
Create a new CSV dataframe (pre-ABC data). This is used for both ABC Analysis and Multi-Criteria Analysis.
```python   
grouped = sales_clean.groupby('PRODUCTCODE').agg(total_sales = ('QUANTITYORDERED',np.sum), total_revenue = ('SALES', np.sum)).reset_index()
grouped.info()
```

Lines 20-21:  
This is used for Multi-Criteria Analysis on a Store-level. For this, classification of Store is Country.
```python   
by_store = sales_clean.groupby(['COUNTRY','PRODUCTCODE']).agg(total_sales = ('QUANTITYORDERED',np.sum), total_revenue = ('SALES',np.sum)).reset_index()
by_store.info()
```

### Part 2 - ABC Analysis

Lines 26-28:  
Perform ABC Analysis on CSV dataframe (pre-ABC data)
```python   
abc = inv.ABC(grouped[['PRODUCTCODE', 'total_sales']])
abc.info()
abc.Category.value_counts()
```

Lines 30-31:  
Plot the charts for ABC Analysis using Seaborn.
```python   
sns.countplot(x = 'Category', data = abc)
sns.barplot(x = 'Category', y = 'total_sales', data = abc)
```

### Part 3 - Multi-Criteria ABC Analysis

Lines 36-38:  
Perform Multi-Criteria ABC Analysis on CSV dataframe (pre-ABC data)
```python   
mc_abc = inv.productmix(grouped['PRODUCTCODE'], grouped['total_sales'], grouped['total_revenue'])
mc_abc.info()
mc_abc.product_mix.value_counts()
```

Lines 40-42:  
Plot the charts for Multi-Criteria ABC Analysis using Seaborn.
```python   
sns.countplot(x = 'product_mix', data = mc_abc)
sns.barplot(x = 'product_mix', y = 'sales', data = mc_abc)
sns.barplot(x = 'product_mix', y = 'revenue', data = mc_abc)
```

### Part 4 - Multi-Criteria ABC Analysis on a Store Level

Lines 47-51:  
Perform Multi-Criteria ABC Analysis on Store-level on CSV dataframe (pre-ABC data)
```python   
mix_country = inv.productmix_storelevel(by_store['PRODUCTCODE'], by_store['total_sales'], by_store['total_revenue'], by_store['COUNTRY'])
mix_country.info()

product_mix = mix_country.groupby(['storeofsku','product_mix']).count().reset_index().iloc[:,0:3]
product_mix.info()
```

Lines 53-54:  
Create a variable for Australia's product mix for analysis.
```python   
australia = product_mix[product_mix.storeofsku == 'Australia']
australia.info()
```

Lines 56:  
Plot the charts for Australia's Multi-Criteria ABC Analysis using Seaborn.
```python   
sns.barplot(x = 'product_mix', y = 'sku', data = australia)
```

## Credit

Sales Data Sample (https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)

## License

[MIT](https://choosealicense.com/licenses/mit/)
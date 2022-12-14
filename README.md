# Multi-Criteria ABC Segmentation

This will demonstrate to you how to perform Multi-Criteria ABC Segmentation using Python.

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

In total, there will be two sets of scripts which make use of ABC Analysis to perform segmentation:

- Product Segmentation
- Supplier Segmentation

## Product Segmentation

Normally, with ABC Analysis, we will classify these SKUs into either one of the three categories:

![ABC Analysis Diagram](https://github.com/dwoo-work/MultiCriteriaABC.Analysis/blob/0a89153bb25bf3f79aac81b93a0df28b6b9eb45a/img/ABC_Analysis_Diagram.png)

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

## Supplier Segmentation

When it comes to Supplier Segmentation, one popular model that is commonly being used, is the Kraljic's Matrix Diagram:

![Kraljic's Matrix Diagram](https://github.com/dwoo-work/MultiCriteriaABC.Analysis/blob/0a89153bb25bf3f79aac81b93a0df28b6b9eb45a/img/Kraljic's_Matrix_Diagram.png)

For each supplier, they are evaluated on two metrics - their products comlexity (risk), and their impact to our business (cost).

To measure risk, we will employ a Risk Rank from 0 (least risky) to 2 (most risky):

| risk factors       | + 0.0 (N)            | + 0.5 (Y)               |
| ------------------ | ---------------------| ----------------------- |
| availability       | regular              | seldom                  |
| suppliers          | many                 | few                     |
| product_complexity | standard             | complex                 |
| price_stability    | stable               | unstable                |

To measure the cost, the formula is shown below:

- Cost = (Cost per unit) * (Total units planned to purchase)

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

For Product Segmentation, you can download the sales_data_sample_utf8.csv file from the source folder, which is located [here](https://github.com/dwoo-work/MultiCriteriaABC.Analysis/blob/main/src).

On the other hand, for Supplier Segmentation, you can download the supplier_data_sample_utf8.csv file from the source folder, which is located [here](https://github.com/dwoo-work/MultiCriteriaABC.Analysis/blob/main/src).

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
sns.countplot(x = 'Category', data = abc).set(title = 'No. of A, B, and C Cat. Items for All Countries')
sns.barplot(x = 'Category', y = 'total_sales', data = abc).set(title = 'Avg. Value of A, B, and C Cat. Items for All Countries')
```

![Plot1](https://github.com/dwoo-work/multi-criteria-abc-segmentation/blob/main/plots/plot1.png)
![Plot2](https://github.com/dwoo-work/multi-criteria-abc-segmentation/blob/main/plots/plot2.png)

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
sns.countplot(x = 'product_mix', data = mc_abc).set(title = 'No. of A_A to C_C Cat. Items for All Countries')
sns.barplot(x = 'product_mix', y = 'sales', data = mc_abc).set(title = 'Avg. Value of A_A to C_C Cat. Items for All Countries')
sns.barplot(x = 'product_mix', y = 'revenue', data = mc_abc).set(title = 'Total Revenue of A_A to C_C Cat. Items for All Countries')
```

![Plot3](https://github.com/dwoo-work/multi-criteria-abc-segmentation/blob/main/plots/plot3.png)
![Plot4](https://github.com/dwoo-work/multi-criteria-abc-segmentation/blob/main/plots/plot4.png)
![Plot5](https://github.com/dwoo-work/multi-criteria-abc-segmentation/blob/main/plots/plot5.png)

### Part 4 - Multi-Criteria ABC Analysis on a Store Level (Australia)

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
sns.barplot(x = 'product_mix', y = 'sku', data = australia).set(title = 'No. of A_A to C_C Cat. Items for Australia')
```

![Plot6](https://github.com/dwoo-work/multi-criteria-abc-segmentation/blob/main/plots/plot6.png)

## Code Explanation (for Supplier Segmentation)

### Part 1 - Preparation

Lines 5-6:  
Import the required libraries.
```python   
import pandas as pd
import seaborn as sns
```

Lines 8-12:  
Import and clean the CSV dataframe.
```python   
supplier = pd.read_csv('https://raw.githubusercontent.com/dwoo-work/multi-criteria-abc-segmentation/main/src/supplier_data_sample_utf8.csv')
supplier = supplier.drop_duplicates()
supplier = supplier.dropna()
supplier.info()
supplier.head()
```

Lines 14-20:  
Convert availability section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present). Then, add all responsed values from Q1 to Q5, to a consolidated availability column within the dataframe.
```python   
supplier['AVAILABILITY_Q1'] = pd.to_numeric(supplier['AVAILABILITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q2'] = pd.to_numeric(supplier['AVAILABILITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q3'] = pd.to_numeric(supplier['AVAILABILITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q4'] = pd.to_numeric(supplier['AVAILABILITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['AVAILABILITY_Q5'] = pd.to_numeric(supplier['AVAILABILITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['AVAILABILITY'] = supplier['AVAILABILITY_Q1'] + supplier['AVAILABILITY_Q2'] + supplier['AVAILABILITY_Q3'] + supplier['AVAILABILITY_Q4'] + supplier['AVAILABILITY_Q5']
```

Lines 22-28:  
Convert suppliers section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present). Then, add all responsed values from Q1 to Q5, to a consolidated suppliers column within the dataframe.
```python   
supplier['SUPPLIERS_Q1'] = pd.to_numeric(supplier['SUPPLIERS_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q2'] = pd.to_numeric(supplier['SUPPLIERS_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q3'] = pd.to_numeric(supplier['SUPPLIERS_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q4'] = pd.to_numeric(supplier['SUPPLIERS_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['SUPPLIERS_Q5'] = pd.to_numeric(supplier['SUPPLIERS_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['SUPPLIERS'] = supplier['SUPPLIERS_Q1'] + supplier['SUPPLIERS_Q2'] + supplier['SUPPLIERS_Q3'] + supplier['SUPPLIERS_Q4'] + supplier['SUPPLIERS_Q5']
```

Lines 30-36:  
Convert product complexity section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present). Then, add all responsed values from Q1 to Q5, to a consolidated product complexity column within the dataframe.
```python   
supplier['PRODUCT_COMPLEXITY_Q1'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q2'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q3'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q4'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRODUCT_COMPLEXITY_Q5'] = pd.to_numeric(supplier['PRODUCT_COMPLEXITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['PRODUCT_COMPLEXITY'] = supplier['PRODUCT_COMPLEXITY_Q1'] + supplier['PRODUCT_COMPLEXITY_Q2'] + supplier['PRODUCT_COMPLEXITY_Q3'] + supplier['PRODUCT_COMPLEXITY_Q4'] + supplier['PRODUCT_COMPLEXITY_Q5']
```

Lines 38-44:  
Convert product complexity section from N or Y, to its 0.0 (risk factor absent) or 0.1 (risk factor present). Then, add all responsed values from Q1 to Q5, to a consolidated product complexity column within the dataframe.
```python   
supplier['PRICE_STABILITY_Q1'] = pd.to_numeric(supplier['PRICE_STABILITY_Q1'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q2'] = pd.to_numeric(supplier['PRICE_STABILITY_Q2'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q3'] = pd.to_numeric(supplier['PRICE_STABILITY_Q3'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q4'] = pd.to_numeric(supplier['PRICE_STABILITY_Q4'].replace(['N', 'Y'], ['0.0', '0.1']))
supplier['PRICE_STABILITY_Q5'] = pd.to_numeric(supplier['PRICE_STABILITY_Q5'].replace(['N', 'Y'], ['0.0', '0.1']))

supplier['PRICE_STABILITY'] = supplier['PRICE_STABILITY_Q1'] + supplier['PRICE_STABILITY_Q2'] + supplier['PRICE_STABILITY_Q3'] + supplier['PRICE_STABILITY_Q4'] + supplier['PRICE_STABILITY_Q5']
```

Lines 46:  
Create the Risk Index variable within the CSV dataframe.
```python   
supplier['risk_index'] = supplier['AVAILABILITY'] + supplier['SUPPLIERS'] + supplier['PRODUCT_COMPLEXITY'] + supplier['PRICE_STABILITY']
```

Lines 48-49:  
Create the Value variable within the CSV dataframe. Low value refers to value below the median level, and high value refers to value above the median level.
```python   
supplier['value'] = supplier['PRICEEACH'] * supplier['QUANTITYORDERED']
supplier.value.describe()
```

Lines 51-52:  
Create a new CSV dataframe (cleaned data).
```python   
supplier_clean = supplier.copy()
supplier_clean.info()
```

### Part 2 - Perform Supplier Segmentation using Karljic's Matrix

Lines 57-72:  
Create a function that defines each supplier in one of the four Kraljic's Matrix quadrants.
```python   
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
```

Lines 74:  
Create a scatter plot for all the suppliers, with different colors for each Kraljic's Matrix quadrants.
```python   
kraljic_diagram = sns.scatterplot(x = 'risk_index', y = 'value', data = supplier_clean, hue= 'category').set(title = 'Suppliers Classification using the Kraljic Matrix')
```

![Plot7](https://github.com/dwoo-work/multi-criteria-abc-segmentation/blob/main/plots/plot7.png)

## Credit

Sales Data Sample (https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)

## License

[MIT](https://choosealicense.com/licenses/mit/)

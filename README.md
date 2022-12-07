# Multi-Criteria ABC Analysis

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

- A: Products / Suppliers / Customers that represent 75% of the business.
- B: Products / Suppliers / Customers that represent 20% of the business.
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

## Code Explanation

Lines X-X:  
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse porta.
```python   
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse porta.
```

## Credit

Sales Data Sample (https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)

## License

[MIT](https://choosealicense.com/licenses/mit/)
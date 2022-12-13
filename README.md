# Product Correlation

An interesting way for markets and stores to improve their sales through the analysis of their history is by identifying the existing correlation between products. This repository presents the implementation of a script in Python that approaches the subject and an example of its applicability.

The dataset used in the application is SupremEats_2011, which is also present in this repository. For a more iterative execution, follow the link of this application on Google Colab: https://colab.research.google.com/drive/15_47qtVwEs7RVNlNZZboD5MvyOlySkCP?usp=sharing

The dataset may not be present in Colab due to automatically performed recycling. For that, it will be necessary to add it for execution.

SupremEats_2011 is composed by tables: Categories, Customers, Employees, Order_Details, Orders, Products, Shippers and Suppliers.

The objective is to identify which pairs of products are usually bought together, so that the market can organize itself strategically to increase sales. Thus, by identifying these pairs, products can be placed next to each other on shelves or promotions and combos can be created, increasing customer interest and inducing them to buy more.

First, we start by importing Pandas and defining it as pd. This means that every time we use pd, we are using Pandas. Pandas is a software library created for the Python language for data manipulation and analysis.

```
import pandas as pd
```

To import a file in .xlsx format we use Pandas ExcelFile() function. If you want to use another one, replace the existing one with the desired one. The imported file is saved in the xls variable. Note: as already said, Colab deletes attached files after a while, so remember to add the dataset.

```
xls = pd.ExcelFile('SupremEats_2011.xlsx')
```

The imported file has several worksheets. So that we can work properly, one option is to transfer each worksheet to a different DataFrame. DataFrames are our data tables, with information distributed in rows and columns. In most of the actions in which we use Pandas, we need our data to be in DataFrame format. Therefore, below each worksheet is transferred to a DataFrame with an indicative name.

```
categories = pd.read_excel(xls, 'Categories')
customers = pd.read_excel(xls, 'Customers')
employees = pd.read_excel(xls, 'Employees')
order_details = pd.read_excel(xls, 'Order_Details')
orders = pd.read_excel(xls, 'Orders')
products = pd.read_excel(xls, 'Products')
shippers = pd.read_excel(xls, 'Shippers')
supliers = pd.read_excel(xls, 'Suppliers')
```

In this code we will mainly work with the DataFrame order_details, so let's visualize it.

```
order_details
```

<p align="center">
<img width="400" src="/Figures/01.png" alt="Figure 01">
</p>

The objective is to identify the correlation between products that are purchased together, so the UnitPrice and Discount columns are not of interest to us. We can delete them through the drop() function. We apply this function to the order_details DataFrame and save it overwriting the previous order_details.

```
order_details = order_details.drop(columns =['UnitPrice','Discount'])
order_details
```

<p align="center">
<img width="300" src="/Figures/02.png" alt="Figure 02">
</p>

It is interesting that we can visualize the data in a more direct way, to find relevant information for decision making. An example is organizing the order_details table data so that we can find the most popular product among customers. The most popular product is the one that appears in the most orders. So, we use the groupy function and aggregate (agg) the data. We will aggregate the data into two columns: orders and quantity. For orders, we will use the OrderID column of the order_details DataFrame, so that it only counts the number of occurrences in different orders using the term nunique. For quantity we will use the Quantity column of the order_details Dataframe and check the total sum of the purchase of each product. We then sort from highest to lowest through the sort_values() function, setting orders as the base column for order determination and setting ascending to False for descending. Finally, we want only the 10 most popular products to be displayed, so we use head(10).

```
order_details.groupby('ProductID').agg(
    orders=('OrderID', 'nunique'),
    quantity=('Quantity', 'sum')
).sort_values(by='orders', ascending=False).head(10)
```

<p align="center">
<img width="300" src="/Figures/03.png" alt="Figure 03">
</p>

Now, to identify the correlation between the products, we need to check how often the products are purchased together. For example, if we want to check if there is a correlation between the sale of bread and jam, we need to check how many times bread and jam appear to be sold in the same order. So, let's create a table where the rows are the orders and the columns are the products. When a product appears in an order, we fill in the corresponding space with the quantity of products purchased. We use the pivot_table() function for this, we identify the rows as the OrderID, the columns as the ProductIDs, the values ​​as the Quantity and fill in with 0 when there is no specific product in the order placed.

```
items_Matrix = order_details.pivot_table(index='OrderID', columns=['ProductID'], values='Quantity').fillna(0)
items_Matrix.head(10)
```

<p align="center">
<img width="700" src="/Figures/04.png" alt="Figure 04">
</p>

Then, continuing the identification of the correlation, let's create a function get_recommendations_id that will receive two parameters: the matrix of items created earlier and the id of the item to discover which product is most correlated. Inside this function we create a recommendations variable. First, let's establish the correlation between the item defined for us to discover and the other products. We use the corrwith() function for this. It checks within the items matrix if there are orders in which the product appears and if there are products that are purchased together with them, and thus creates a vector establishing the relationship of this product with the others, so that each line is a relationship value of this product with another product. Then, we delete all null values ​​from this vector using the dropna() function. The next line creates a column called correlation and resets the vector indices (reset_index()), restarting the index count keeping the current shape of the vector. Then, the vector is reordered in descending order, putting the highest correlation first, the second highest second, and so on. The vector indices are reset again, keeping the current form, that is, keeping the sort descending order. Finally, the value returned by the function is row 1 of the ProductID column, which corresponds exactly to the product ID with the highest correlation with the analyzed product. We did not use line 0 because it is the correlation with the product itself, which is equivalent to 100%.

```
def get_recommendations_id(matrix, item):
    
    recommendations = matrix.corrwith(matrix[item])
    recommendations.dropna(inplace=True)
    recommendations = pd.DataFrame(recommendations, columns=['correlation']).reset_index()
    recommendations = recommendations.sort_values(by='correlation', ascending=False)
    recommendations = recommendations.reset_index()
    
    return recommendations['ProductID'][1]
```

Then we repeat the same function, but the goal now is to return the correlation value between the desired product and the product with which it is most correlated.

```
def get_recommendations_correlation(df, item):
    
    recommendations = df.corrwith(df[item])
    recommendations.dropna(inplace=True)
    recommendations = pd.DataFrame(recommendations, columns=['correlation']).reset_index()
    recommendations = recommendations.sort_values(by='correlation', ascending=False)
    recommendations = recommendations.reset_index()
    
    return recommendations['correlation'][1]
```

For better organization, let's create a DataFrame called products_correlation, where we will save all results. First, we create this DataFrame as a copy of Dataframe products. Then we delete all the unwanted columns, keeping only the ProductID and ProductName columns. To delete columns, we use the drop() function and define the columns to be deleted through their names.

```
products_correlation = products
products_correlation = products_correlation.drop(columns=['SupplierID', 'CategoryID', 'QuantityPerUnit', 'UnitPrice', 'UnitsInStock','UnitsOnOrder','ReorderLevel','Discontinued'])
```

Now, let's create a Recommendation column. The idea is to run the get_recommendations_id function for all ProductIDs and identify the most recommended product ID to buy for each one. So we save these ID values in a table on the right. For this, we use the apply() function. Through it, we apply a lambda and determine an x. As the lambda is running on products_correlation['ProductID'], this means that a loop is executed so that at each round of the loop, the x is equivalent to one of the values of the ProductID column of the products_correlation DataFrame. After the : we determine that it will be executed in this loop which, in this case, is the function get_recommendations_id, which receives the array of items and the x. So, in summary, a loop is executed over the function so that it receives in each round of the loop the product matrix and one of the 77 products so that it is possible to calculate the product most correlated to each of the 77 products. All these values are automatically saved in the new Recommendation column of the DataFrame products_correlation.

```
products_correlation['Recommendation'] = products_correlation['ProductID'].apply(lambda x: get_recommendations_id(items_Matrix, x))
```

We can check how the DataFrame products_correlation looks now.

<p align="center">
<img width="500" src="/Figures/05.png" alt="Figure 05">
</p>

We can also check which products appear more as correlations through the .value_counts() function. Thus, we can determine products that are compatible with several products, instead of just one. Using head(10) it is possible to identify the first 10 responses. If you want to view them all, just remove the head(10) from the line of code.

```
products_correlation['Recommendation'].value_counts().head(10)
```

<p align="center">
<img width="400" src="/Figures/06.png" alt="Figure 06">
</p>

Another interesting piece of information to be displayed in our products_correlation DataFrame is the product name corresponding to the correlation ID. For this, let's again use apply() to create a new NameRecommendation column. As we already have the ID list of all products and their respective names, we use the DataFrame products_correlation itself as a reference and apply the set_index function to define the ProductID column as a base and say through the loc function that we want to find all ProductNames referring to the IDs of the Recommendation column, which in this case are the values that will replace the x in the loop.

```
products_correlation['NameRecommendation'] = products_correlation['Recommendation'].apply(lambda x: products.set_index('ProductID').loc[x, 'ProductName'])
```

Again, let's check how our products_correlation DataFrame is.

<p align="center">
<img width="700" src="/Figures/07.png" alt="Figure 07">
</p>

Finally, the last thing left to complete the DataFrame products_correlation is the correlation value. Through it we can define whether the correlation is interesting or not. Again, we apply the apply() function to create a new column: Correlation. This time, though, we'll apply it to the get_recommendations_correlation() function we created earlier.

```
products_correlation['Correlation'] = products_correlation['ProductID'].apply(lambda x: get_recommendations_correlation(items_Matrix, x))
```

Thus, we can admire the final result of our work: a table containing the list of product IDs, their names, the products they most correlate with and the correlation value.

```
products_correlation
```

<p align="center">
<img width="800" src="/Figures/08.png" alt="Figure 08">
</p>

To complement this, we can sort this table in descending order using the Correlation column as a base, as we have done before in this same code.

```
products_correlation = products_correlation.sort_values(by='Correlation', ascending=False)
products_correlation
```

<p align="center">
<img width="800" src="/Figures/09.png" alt="Figure 09">
</p>

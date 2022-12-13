# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 13:58:41 2022

@author: Marcony Montini
"""

import pandas as pd

xls = pd.ExcelFile('SupremEats_2011.xlsx')

categories = pd.read_excel(xls, 'Categories')
customers = pd.read_excel(xls, 'Customers')
employees = pd.read_excel(xls, 'Employees')
order_details = pd.read_excel(xls, 'Order_Details')
orders = pd.read_excel(xls, 'Orders')
products = pd.read_excel(xls, 'Products')
shippers = pd.read_excel(xls, 'Shippers')
supliers = pd.read_excel(xls, 'Suppliers')

order_details

order_details = order_details.drop(columns =['UnitPrice','Discount'])
order_details

order_details.groupby('ProductID').agg(
    orders=('OrderID', 'nunique'),
    quantity=('Quantity', 'sum')
).sort_values(by='orders', ascending=False).head(10)

items_Matrix = order_details.pivot_table(index='OrderID', columns=['ProductID'], values='Quantity').fillna(0)
items_Matrix.head(10)

def get_recommendations_id(matrix, item):
    
    recommendations = matrix.corrwith(matrix[item])
    recommendations.dropna(inplace=True)
    recommendations = pd.DataFrame(recommendations, columns=['correlation']).reset_index()
    recommendations = recommendations.sort_values(by='correlation', ascending=False)
    recommendations = recommendations.reset_index()
    
    return recommendations['ProductID'][1]

def get_recommendations_correlation(df, item):
    
    recommendations = df.corrwith(df[item])
    recommendations.dropna(inplace=True)
    recommendations = pd.DataFrame(recommendations, columns=['correlation']).reset_index()
    recommendations = recommendations.sort_values(by='correlation', ascending=False)
    recommendations = recommendations.reset_index()
    
    return recommendations['correlation'][1]

products_correlation = products

products_correlation = products_correlation.drop(columns=['SupplierID', 'CategoryID', 'QuantityPerUnit', 'UnitPrice', 'UnitsInStock','UnitsOnOrder','ReorderLevel','Discontinued'])

products_correlation['Recommendation'] = products_correlation['ProductID'].apply(lambda x: get_recommendations_id(items_Matrix, x))
products_correlation

products_correlation['Recommendation'].value_counts().head(10)

products_correlation['NameRecommendation'] = products_correlation['Recommendation'].apply(lambda x: products.set_index('ProductID').loc[x, 'ProductName'])
products_correlation

products_correlation['Correlation'] = products_correlation['ProductID'].apply(lambda x: get_recommendations_correlation(items_Matrix, x))
products_correlation

products_correlation = products_correlation.sort_values(by='Correlation', ascending=False)
products_correlation

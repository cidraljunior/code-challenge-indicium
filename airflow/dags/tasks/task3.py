import collections
from numpy import product
import pandas as pd
from pymongo import MongoClient

date = "2021-01-01"

#Extract local data
orders = pd.read_csv("/data/postgres/orders/{0}/data.csv".format(date))
products = pd.read_csv("/data/postgres/products/{0}/data.csv".format(date))
order_details = pd.read_csv("/data/csv/{0}/data.csv".format(date))

#Transform
orders = orders[['order_id','order_date','customer_id']].set_index('order_id')
products = products[['product_id','product_name']].set_index('product_id')
order_details = order_details.join(products, on = 'product_id')

data = []

for order_id in order_details.order_id.unique():
    json = order_details[order_details.order_id == order_id].drop("order_id", axis = 1).to_dict("records")
    
    order = {
        "order_id": order_id,
        #"order_date": orders[order_id]['order_date'],
        "products": json
    }
    data.append(order)

details = pd.DataFrame(data).to_dict("records")

#print(order)

# Load to Database
client =  MongoClient('mongo-container', 27017, username='dharma', password = '4815162342')

db = client['orders']
collection = db['details']

collection.insert_many(details)

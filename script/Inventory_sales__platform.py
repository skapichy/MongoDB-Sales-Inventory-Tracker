# Importing libraries needed for the project

from pymongo import MongoClient
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Connecting to mongodb client and creating a database
client = MongoClient("mongodb://localhost:27017/")
db = client["marketmart_db"]

# Initializing the faker library to generate sample data
fake = Faker()

import pprint as pp

# This code is used as a unified print to run my code in a list format
def print_result(cursor):
    _list = list(cursor)
    len_list = len(_list)
    print(f"Total documents: {len_list}") 
    pp.pprint(_list)
    
# database list of collections
products_collection = db["products"]
sales_collection = db["sales"]
inventory_collection = db["Inventory"]
customers_collection = db["Customers"]
restock_logs_collection = db["RestockLogs"]

# Creating of products collections to house the product data & creation of a sample document structure
products_collection = db["products"]

products_data = {
    "_id": 1,
    "productID": "PROD001",
    "name": "Paracetamol 500mg",
    "category": "Health",
    "price": 100,
    "supplier": "JamesVendor",
    "unit": "pack",
    "createdAt": datetime(2023,1,1),
    "isActive": True
}
result = products_collection.insert_one(products_data)
print(f"Document Inserted ID:", result.inserted_id)


# Creating of sales collections to house the product data & creation of a sample document structure
sales_collection = db["sales"]

sales_data = {
    "_id": 1,
    "sales_id": "SAL_01",
    "customerID": "CUST005",
    "items": [{
        "productID": "PROD001", 
        "quantity": 2, 
        "unitprice": 100
    }],
    "totalAmount": 200,
    "salesDate": datetime(2023,1,1,13,50,31),
    "paymentMethod": "Cash"
}
result = sales_collection.insert_one(sales_data)
print("Document Inserted ID:", result.inserted_id)    


# Task Insert 30 products data
# Data generated which is inserted into the products_collection 

product_names = [
    "Paracetamol 500mg","Vitamin C Tablets", "Cough Syrup","Ibuprofen 200mg", "Antacid Tablets", "Toothpaste 100ml",
    "Toothbrush Medium","Shampoo 250ml", "Body Lotion", "Antiseptic Liquid", "Bottled Water 75cl", "Orange Juice 1L",
    "Soft Drink Can","Energy Drink","Chocolate Milk","Laundry Detergent", "Toilet Paper (4 rolls)", "Rice 5kg", "Cooking Oil 1L","Margarine 250g"]

categories = ["Health", "Personal Care","Beverages", "Household", "Groceries","Baby Care","Snacks", "Stationery","Cleaning Supplies","Pet Supplies"]
suppliers = [ "JamesVendor","HealthFirst Supplies","FreshDrop Distributors", "CarePlus Wholesale"]
units = [ "pack","bottle","can", "sachet","piece"]

# Collect products into a list
products_data = []

for i in range(40):
    product = {
        "_id": i + 2,
        "productID": f"PROD{str(i + 2).zfill(3)}",
        "name": random.choice(product_names),
        "category": random.choice(categories),
        "supplier": random.choice(suppliers),
        "price": round(random.uniform(200, 1500), 2),
        "unit": random.choice(units),
        "createdAt": datetime.now() - timedelta(days=random.randint(1, 720)),
        "isActive": True
    }
    products_data.append(product)

# Insert all documents at once
result = products_collection.insert_many(products_data)
print(f"Inserted {len(result.inserted_ids)} documents.")

# Fetch and print all inserted products
all_products = list(products_collection.find())
print("Total documents:", len(all_products))
for product in all_products:
    print(product)
    

# Task Insert 50 sales records
# Data generated which is inserted into the sales_collection 

# collect sales data into a list
sales_data = []

for i in range(50):
    # 🔹 Pick a random product
    product = products_collection.aggregate([{"$sample": {"size": 1}}]).next()
    
    quantity = random.randint(1, 4)
    unitprice = product["price"]
    product_id = product["productID"]
    total = quantity * unitprice

    sales = {
        "_id": i + 2,
        "sales_id": f"SAL_02{i+1}",
        "customerID": f"CUST{str(random.randint(1, 20)).zfill(3)}",
        "items": [{
            "productID": product_id,
            "quantity": quantity,
            "unitprice": unitprice,
            "totalAmount": total
        }],
        "totalAmount": total,
        "salesDate": datetime.now() - timedelta(days=random.randint(1, 720)),
        "paymentMethod": random.choice(["cash", "transfer", "card"])
    }
    sales_data.append(sales)
    
# Insert all documents at once
result = sales_collection.insert_many(sales_data)
print(f"Inserted {len(result.inserted_ids)} documents.")

# Fetch and print all inserted products
all_sales = list(sales_collection.find())
print("Total documents:", len(all_sales))
for sale in all_sales:
    print(sale)    
    

# Task Insert 50 sales records
# Data generated which is inserted into the sales_collection 

# Creation of Database for customers
customers_collection = db["Customers"]

# Get unique customer IDs from sales
customer_ids = sales_collection.distinct("customerID")

customers = []

for cust_id in customer_ids:
    customer = {
        "customerID": cust_id,
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "gender": random.choice(["male", "female"]),
        "dateOfBirth": datetime.combine(
            fake.date_of_birth(minimum_age=18, maximum_age=65), datetime.min.time()
        ),  # 👈 Fix applied here
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "postalCode": fake.postcode(),
            "country": "Nigeria"
        },
        "joinedDate": datetime.now() - timedelta(days=random.randint(30, 800)),
        "loyaltyPoints": random.randint(0, 500),
        "isActive": True,
        "preferredPaymentMethod": random.choice(["cash", "card", "transfer"])
    }
    customers.append(customer)

# Insert all customers
customers_collection.insert_many(customers)

# Print all inserted customers
all_customers = list(customers_collection.find())
print("Total documents:", len(all_customers))
for cust in all_customers:
    print(cust)    


# Task Insert inventory records
# Data generated which is inserted into the inventory_collection 

# Fetch full product documents instead of only distinct productIDs
products = list(products_collection.find())

# Create Inventory collection
inventory_collection = db["Inventory"]

inventory_docs = []
for p in products:
    inventory_docs.append({
        "productID": p["productID"],
        "stockLevel": random.randint(20, 200),
        "reorderLevel": random.randint(10, 50),
        "lastRestocked": datetime.now() - timedelta(days=random.randint(1, 30))
    })

# Insert inventory documents
inventory_collection.insert_many(inventory_docs)

# Print all inserted inventory docs
all_inventory = list(inventory_collection.find())
print("Total documents:", len(all_inventory))
for invent in all_inventory:
    print(invent)
    

# Task Insert restocked records
# Data generated which is inserted into the restock_logs_collection 

# Fetch all products
products = list(products_collection.find())

# Create the restock logs collection
restock_logs_collection = db["RestockLogs"]

# Prepare restock log documents
restock_logs = []

for p in products:
    for i in range(10 + random.randint(0, 5)):  # 10 to 15 logs per product
        restock_logs.append({
            "productID": p["productID"],
            "restockDate": datetime.now() - timedelta(days=random.randint(10, 300)),
            "quantityAdded": random.randint(20, 100),
            "supplier": p["supplier"],
            "restockedBy": fake.name()
        })

# Insert all restock logs
restock_logs_collection.insert_many(restock_logs)

# Print summary
print(f"Inserted {len(restock_logs)} restock logs.")
# Print all inserted courses
restocks_log = list(restock_logs_collection.find())
print("Total documents:", len(restock_logs))
for log in restock_logs:
    print_result(log)       
    
    
# Task: Add a new product to the product collection

# create a function
def add_product(name, category,supplier,price,unit, isActive = True):
    
    # fetch the last _id inserted into the collectioon to avoid duplicate
    last_product = products_collection.find_one(sort = [("_id", -1)]) # -1 is descending number
    
    # create a new unique _id 
    new_id = last_product["_id"] + 1 if last_product else 1
    
    # Generate productID
    productID = f"PROD{str(new_id).zfill(3)}"
    
    # Here is the code
    product = {
        "_id": new_id,
        "productID": productID,
        "name": name,
        "category": category,
        "supplier": supplier,
        "price": round(price, 2),
        "unit": unit,
        "createdAt": datetime.now(),
        "isActive": isActive
    }

    # Insert all documents at once
    result = products_collection.insert_one(product)
    print(f"Inserted product with _id: {result.inserted_id}")

resp = add_product("Dettol Soap", "Personal Care", "FreshSupplier", 299.99, "bar")
print(resp)


# Task: Create a function to add a new sale with a unique sale ID and link to an existing or random customer.

# create a function
def new_sale(productID, quantity, customerID = None):
    
    # Get product by productID
    product = products_collection.find_one({"productID": productID})
    if not product:
        print("product not found")
        return
    
    # Extract price and calculate totalAmount
    unitprice = product["price"]
    totalAmount = round(quantity * unitprice, 2)
    
    # fetch the last _id inserted into the collectioon to avoid duplicate
    last_sale = sales_collection.find_one(sort = [("_id", -1)]) # -1 is descending number
    
    # create a new unique _id 
    new_id = last_sale["_id"] + 1 if last_sale else 1
    
    # Generate productID
    saleID = f"SAL{str(new_id).zfill(2)}"
    
   # If customerID is not provided, randomly select from existing customers
    if not customerID:
        customers = customers_collection.distinct("customerID")
        if not customers:
            print(" No customers available.")
            return
        customerID = random.choice(customers)

     # Create the sale document
    sale = {
        "_id": new_id,
        "saleID": saleID,
        "customerID": customerID,
        "items": [{
            "productID": productID,
            "quantity": quantity,
            "unitprice": unitprice,
            "totalAmount": totalAmount
        }],
        "totalAmount": totalAmount,
        "saleDate": datetime.now(),
        "paymentMethod": random.choice(["cash", "transfer", "card"])
    }
    # Insert into collection
    result = sales_collection.insert_one(sale)
    print(f"New SaleID added: {result.inserted_id}")

# An example without a customer1D    
resp = new_sale("PROD012", 3)
print(resp)

# An example with a customer1D    
respP = new_sale("PROD015", 4, "CUST005")
print(respP)


# Task: Create a function to update stock level of a product less than 100 after restocking.

# create a function
def update_stock_level(quantityAdded=None): 
    
    # Find one random product with stockLevel < 100
    low_stock_item = inventory_collection.find_one({"stockLevel": {"$lt": 100}})
    if not low_stock_item:
        print("Low-stock inventory not found")
        return
    
    # Generate a random restock amount if not provided
    if quantityAdded is None:
        quantityAdded = random.randint(50, 100)
    
    # Update stockLevel and lastRestocked
    inventory_collection.update_one(
        {"productID": low_stock_item["productID"]}, {
            "$inc": {"stockLevel": quantityAdded},
            "$set": {"lastRestocked": datetime.now()}
        }
    )
    
    # Log the restock action in RestockLogs collection
    restock_log = {
        "productID": low_stock_item["productID"],
        "restockDate": datetime.now(),
        "quantityAdded": quantityAdded,
        "supplier": products_collection.find_one({"productID": low_stock_item["productID"]}).get("supplier", "Unknown"),
        "restockedBy": fake.name()
    }
    
    restock_logs_collection.insert_one(restock_log)

    print(f" Restocked '{low_stock_item['productID']}' with +{quantityAdded} units.")
update_stock_level()


# Task: Create a function to deactivate a product.

def deactivate_product(productID):
    
    # find the product
    product = products_collection.find_one({"productID": productID})
    if not product:
        print(f"product with ID '{productID}' not found.")
        return
    
    # Deactivate the product change isActive from True to False
    products_collection.update_one(
        {"productID": productID},
        {"$set": {"isActive": False}}
    )
    
    print(f"Product '{productID}' has been deactivated")
    
resp = deactivate_product("PROD011")    
resp


# Task: Create a function to retrieve all active products below reorder level.

def get_active_lowstock_products():
    
    # we are joining two collections together reorder level(inventory) & active products from (products)
    # Join inventory with products on productID
    
    pipeline = [
        {
            "$lookup": {
                "from": "products", # collection to join
                "localField": "productID", # Field in inventory
                "foreignField": "productID",  # Field in product
                "as": "productInfo"  # New field name to store the joined data as an array
            }
        },
        {
           "$unwind": "$productInfo"  # Flatten the joined product info 
        },
        {
            "$match": {
                "productInfo.isActive": True,
                "$expr": { # $expr allows you to compare two fields inside the same document, rather than field vs value.
                    "$lt": ["$stocklevel", "$reorderLevel"]
                }
            }
        },
        {
            "$project": {
                "_id": 0, # 0 means the field should not appear in our result query
                "productID": 1, # 1 means this field should appear in the query
                "stockLevel": 1,
                "reorderLevel": 1,
                "name": "$productInfo.name",
                "category": "$productInfo.category",
                "supplier": "$productInfo.supplier"
            }
        }
    ]
    results = list(inventory_collection.aggregate(pipeline))
    
    if results:
        print("Active Products below Reorder Level: ")
        for product in results:
            print(product)
            
    else:
        print("No active products are below the reorder level.")      
    

resp = get_active_lowstock_products()
resp


# Task Find the top 5 most sold products by total quantity.

pipeline = [
    {"$unwind": "$items"}, # Break sales.items array into individual documents
    {
        "$group": {
            "_id": "$items.productID",    # Group by productID
            "total_quantity_sold": {"$sum": "$items.quantity"}
        }
    },
    { "$sort": {"total_quantity_sold": -1}},   # # Sort by quantity sold, descending
    {"$limit": 5 }  # Top 5 
]

top_products = list(sales_collection.aggregate(pipeline))
for product in top_products:
    print(product)
    

# Task: List all products where current stock is below the reorder level.

low_stock_products = inventory_collection.find({
    "$expr": { "$lt": ["$stockLevel", "$reorderLevel"]}
})
for product in low_stock_products:
    print(product)
    

# Task: Calculate total sales revenue per category.

pipeline = [
    # Break the 'items' array in sales
    {"$unwind": "$items"},
      
    # Join with Products collection to get category
    {"$lookup": {
        "from": "products",
        "localField": "items.productID",
        "foreignField": "productID",
        "as": "productInfo"
        }},
    {"$unwind": "$productInfo"},
    
    # Group by category and productInfo
    {
        "$group": {
            "_id": "$productInfo.category",
            "total_revenue": {
                "$sum": {"$multiply": ["$items.quantity", "$items.unitprice"]}
            }
        }
      },
    {"$sort": {"total_revenue": -1}}
]

category_sales = list(sales_collection.aggregate(pipeline))
for cate in category_sales:
    print(f"Category: {cate['_id']}, Revenue: ₦{round(cate['total_revenue'], 2)}")   
    
    
# Task : Show monthly sales trends (month vs total sales).

pipeline = [
    {
        "$group": {
            "_id": {
                "year": { "$year": "$salesDate" },
                "month": { "$month": "$salesDate" }
            },
            "monthly_sales": { "$sum": "$totalAmount" }
        }
    },
    {
        "$sort": {
            "_id.year": 1,
            "_id.month": 1
        }
    }
]

monthly_trends = list(sales_collection.aggregate(pipeline))

# 🔽 Print results in readable format
for month in monthly_trends:
    year = month["_id"]["year"]
    mth = month["_id"]["month"]
    sales = round(month["monthly_sales"], 2)
    print(f"{year}-{str(mth).zfill(2)}: ₦{sales}")
    

# Task: Identify products with no sales in the last 6 months.

# Calculate date 6 months ago
six_month_ago = datetime.now() - timedelta(days=180)

# Get all productIDs sold in the last 6 months
sold_products = sales_collection.aggregate([
    { "$match": { "salesDate": { "$gte": six_month_ago } } },
    { "$unwind": "$items" },
    { "$group": { "_id": "$items.productID" } }
])

sold_product_ids = [doc["_id"] for doc in sold_products]

# 3. Find products not in the list above
unsold_products = products_collection.find({
    "productID": { "$nin": sold_product_ids } # $nin means not in
})

# 4. Print the unsold products
print("Products with NO sales in the last 6 months:")
for product in unsold_products:
    print(f"- {product['productID']}: {product['name']}")
    

# Task: calculate average sale value per customer.

pipeline = [
    
    # Only keeps documents where totalAmount is not None, Think of it like cleaning bad data.
    {
        "$match": {
            "totalAmount": { "$ne": None }
        }
    },
     
    {
        "$group": {
            "_id": "$customerID", # Group by customer.
            "totalSpent": { "$sum": "$totalAmount" }, # Add up how much each customer spent.
            "numberOfSales": { "$sum": 1 } # Count how many times each customer bought something.
        }
    },
    {
        "$project": {
            "_id": 0,
            "customerID": "$_id", # Renames _id to customerID
            "totalSpent": 1,
            "numberOfSales": 1,
            "averageSaleValue": {
                "$cond": {
                    "if": { "$eq": ["$numberOfSales", 0] },
                    "then": None,
                    "else": { "$round": [{ "$divide": ["$totalSpent", "$numberOfSales"] }, 2] }
                }
            }
        }
    }
]

avg_sales_per_customer = list(sales_collection.aggregate(pipeline))

for customer in avg_sales_per_customer:
    print(f"Customer: {customer['customerID']} | Avg Sale: ₦{customer['averageSaleValue']}")
    
    
# Task: Identify the most common payment method used.

pipeline = [
    {"$group": {
            "_id": "$paymentMethod",
            "count": { "$sum": 1 }}},
    {"$sort": { "count": -1 }},
    {"$limit":1}
]

most_common_method = list(sales_collection.aggregate(pipeline))

if most_common_method:
    method = most_common_method[0]
    print(f"Most common payment method: {method['_id']} (used {method['count']} times)")
else:
    print("No payment methods found.")


#Task: create a visual for Sales trends over time

# Aggregation Pipeline for Monthly Sales Trends
pipeline = [
    {
        "$group": {
            "_id": {
                "year": {"$year": "$salesDate"},
                "month": {"$month": "$salesDate"}
            },
            "totalSales": {"$sum": "$totalAmount"}
        }
    },
    { "$sort": {"_id.year": 1, "_id.month": 1} }
]

# Run aggregation and load into DataFrame
result = list(sales_collection.aggregate(pipeline))
df = pd.DataFrame(result)

# 🛠 Format DataFrame
df["year"] = df["_id"].apply(lambda x: x["year"])
df["month"] = df["_id"].apply(lambda x: x["month"])
df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
df.drop(columns=["_id"], inplace=True)
df.sort_values("date", inplace=True)

# 📈 Plot the Monthly Sales Trend
plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["totalSales"], marker='o', linestyle='-', color='green')
plt.title("📅 Monthly Sales Trend", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Total Sales (₦)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#Task: create a visual for Low stock alerts

# Aggregation pipeline: find low stock products
pipeline = [
    {
        "$match": {
            "$expr": { "$lt": ["$stockLevel", "$reorderLevel"] }
        }
    },
    {
        "$lookup": {
            "from": "Products",
            "localField": "productID",
            "foreignField": "productID",
            "as": "productInfo"
        }
    },
    { "$unwind": "$productInfo" },
    {
        "$project": {
            "productID": 1,
            "stockLevel": 1,
            "reorderLevel": 1,
            "name": "$productInfo.name",
            "category": "$productInfo.category"
        }
    }
]

# Run aggregation and convert to DataFrame
result = list(inventory_collection.aggregate(pipeline))
df = pd.DataFrame(result)

# If there are results, plot the low stock products
if not df.empty:
    plt.figure(figsize=(10, 6))
    plt.barh(df["name"], df["stockLevel"], color='tomato')
    plt.axvline(df["reorderLevel"].mean(), color='blue', linestyle='--', label='Avg Reorder Level')
    plt.title("⚠️ Low Stock Alert: Products Below Reorder Level", fontsize=14)
    plt.xlabel("Stock Level")
    plt.ylabel("Product Name")
    plt.tight_layout()
    plt.legend()
    plt.show()
else:
    print("No products are below the reorder level.")
    

#Task: create a visual for category revenue

# Aggregation pipeline
pipeline = [
    { "$unwind": "$items" },
    {
        "$lookup": {
            "from": "Products",
            "localField": "items.productID",
            "foreignField": "productID",
            "as": "productInfo"
        }
    },
    { "$unwind": "$productInfo" },
    {
        "$group": {
            "_id": "$productInfo.category",
            "total_revenue": {
                "$sum": {
                    "$multiply": ["$items.quantity", "$items.unitprice"]
                }
            }
        }
    },
    { "$sort": { "total_revenue": -1 } }
]

# Run aggregation and convert to DataFrame
result = list(sales_collection.aggregate(pipeline))
df = pd.DataFrame(result)

# Plot category-wise revenue
if not df.empty:
    plt.figure(figsize=(10, 6))
    plt.bar(df["_id"], df["total_revenue"], color='mediumseagreen')
    plt.title("💰 Category-Wise Revenue", fontsize=14)
    plt.xlabel("Category")
    plt.ylabel("Total Revenue (₦)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("No data available to plot.")        
                          
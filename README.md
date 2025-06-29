# MongoDB-Sales-Inventory-Tracker
This project uses MongoDB to simulate a sales and inventory tracking system for a small retail business, like a supermarket or pharmacy. It reflects real-life operations by managing key elements such as products, customers, suppliers, inventory, sales, and restocking activities.

## Project Overview
- MongoDB schema design and data modeling
- Data generation using Python and Faker
- CRUD operations
- Aggregation pipelines for business insights
- Inventory and sales management
  
---
##  Project Setup Instructions
### Install Dependencies 
- Ensure Python is installed. Then install required packages:
- pip install pymongo notebook

### Import libraries.
- from pymongo import MongoClient
- from datetime import datetime, timedelta
- import matplotlib.pyplot as plt
- import seaborn as sns
- from faker import Faker
- import pandas as pd
- import random

### Tech Stack
- MongoDB
- Python (with pymongo)
- Pandas, Matplotlib, Seaborn – for data analysis and visualization
- Faker – for generating synthetic user and course data
- Jupyter Notebook – for interactive documentation and code execution
- random – for generating synthetic random user and course data

### Start MongoDB Server
- Ensure MongoDB is running locally or update your connection string in the .py and .ipynb files: 
- client = MongoClient("mongodb://localhost:27017/")

### Run the Interactive Notebook
- jupyter notebook inventory_sales_analytics_platform.ipynb

### Run Python File (for backup queries)
- python inventory_sales_platform.py

---
## Connection and Database Setup
### Connection to MongoClient
- client = MongoClient("mongodb://localhost:27017/")
- db = client["marketmart_db"]

### Creation of collections to store Data
- products_collection = db["products"]
- sales_collection = db["sales"]
- inventory_collection = db["Inventory"]
- customers_collection = db["Customers"]
- restock_logs_collection = db["RestockLogs"]

---
## Database Schema Documentation
```python
**Products Collection**
products_data = {
    "_id": 1,
    "productID": "PROD001",
    "name": "Paracetamol 500mg",
    "category": "Health",
    "price": 100,
    "supplier": "JamesVendor",
    "unit": "pack",
    "createdAt": datetime(2023,1,1),
    "isActive": True}

**Sales Collection**
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
    "paymentMethod": "Cash"}

**Inventory Collection**
inventory = {
        "productID": p["productID"],
        "stockLevel": random.randint(20, 200),
        "reorderLevel": random.randint(10, 50),
        "lastRestocked": datetime.now() - timedelta(days=random.randint(1, 30))}

**Restocks Collection**
restock_logs = {
            "productID": p["productID"],
            "restockDate": datetime.now() - timedelta(days=random.randint(10, 300)),
            "quantityAdded": random.randint(20, 100),
            "supplier": p["supplier"],
            "restockedBy": fake.name()}

**Customers Collection**
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

```
    
---
### CRUD Functions
- Add new product to the collection
- Add new sale (with unique sales_id and linked customer)
- Update product stock on restock
- Deactivate a product
- Query products below reorder level

### Data Analysis & Aggregation
- Top 5 most sold products
- Products below reorder level
- Total revenue by category
- Monthly sales trends
- Products with no sales in last 6 months
- Average sale value per customer
- Most used payment method



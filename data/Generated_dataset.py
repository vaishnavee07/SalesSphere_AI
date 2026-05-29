import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# =========================================================
# INITIALIZATION
# =========================================================

fake = Faker()

NUM_RECORDS = 100000

# =========================================================
# MASTER DATA
# =========================================================

cities = [
    "Chennai", "Bangalore", "Mumbai", "Delhi",
    "Hyderabad", "Pune", "Kolkata", "Ahmedabad",
    "Coimbatore", "Jaipur"
]

states = {
    "Chennai": "Tamil Nadu",
    "Bangalore": "Karnataka",
    "Mumbai": "Maharashtra",
    "Delhi": "Delhi",
    "Hyderabad": "Telangana",
    "Pune": "Maharashtra",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Coimbatore": "Tamil Nadu",
    "Jaipur": "Rajasthan"
}

genders = ["Male", "Female"]

membership_levels = [
    "Silver",
    "Gold",
    "Platinum"
]

payment_methods = [
    "UPI",
    "Cash",
    "Credit Card",
    "Debit Card",
    "Net Banking"
]

seasons = [
    "Summer",
    "Winter",
    "Monsoon",
    "Festival"
]

product_categories = {

    "Beverages": [
        "Coke", "Pepsi", "Sprite", "Frooti", "Red Bull"
    ],

    "Snacks": [
        "Lays", "Kurkure", "Doritos", "Bingo", "Pringles"
    ],

    "Personal Care": [
        "Shampoo", "Soap", "Toothpaste",
        "Face Wash", "Body Lotion"
    ],

    "Dairy": [
        "Milk", "Butter", "Cheese",
        "Curd", "Paneer"
    ],

    "Household": [
        "Detergent", "Dishwash",
        "Cleaner", "Air Freshener",
        "Floor Cleaner"
    ]
}

# =========================================================
# PRICE RANGES
# =========================================================

price_ranges = {

    "Beverages": (20, 150),

    "Snacks": (10, 200),

    "Personal Care": (50, 500),

    "Dairy": (25, 250),

    "Household": (80, 700)
}

# =========================================================
# DATA STORAGE
# =========================================================

dataset = []

start_date = datetime(2023, 1, 1)

# =========================================================
# DATA GENERATION
# =========================================================

for i in range(NUM_RECORDS):

    # -----------------------------------------------------
    # CUSTOMER FEATURES
    # -----------------------------------------------------

    customer_id = f"CUST{i+1:07d}"

    customer_name = fake.name()

    age = int(np.random.normal(35, 10))

    age = max(18, min(age, 65))

    gender = random.choice(genders)

    city = random.choice(cities)

    state = states[city]

    # Realistic income distribution
    income = int(np.random.normal(70000, 30000))

    income = max(15000, min(income, 300000))

    membership = random.choices(
        membership_levels,
        weights=[60, 30, 10]
    )[0]

    loyalty_score = random.randint(1, 100)

    purchase_frequency = int(
        np.random.exponential(scale=6)
    )

    purchase_frequency = max(1, min(purchase_frequency, 30))

    customer_rating = round(
        random.uniform(2.0, 5.0),
        1
    )

    # -----------------------------------------------------
    # PRODUCT FEATURES
    # -----------------------------------------------------

    category = random.choice(
        list(product_categories.keys())
    )

    product_name = random.choice(
        product_categories[category]
    )

    base_price = round(
        random.uniform(
            price_ranges[category][0],
            price_ranges[category][1]
        ),
        2
    )

    quantity = random.randint(1, 10)

    discount_percentage = random.choice(
        [0, 5, 10, 15, 20, 25, 30, 40]
    )

    inventory_level = random.randint(20, 1500)

    # -----------------------------------------------------
    # TIME FEATURES
    # -----------------------------------------------------

    season = random.choice(seasons)

    festival = 1 if season == "Festival" else 0

    weekend = random.choice([0, 1])

    random_days = random.randint(0, 730)

    order_date = start_date + timedelta(days=random_days)

    # -----------------------------------------------------
    # TRANSACTION FEATURES
    # -----------------------------------------------------

    payment_method = random.choices(
        payment_methods,
        weights=[45, 20, 15, 15, 5]
    )[0]

    # -----------------------------------------------------
    # BUYING LOGIC
    # -----------------------------------------------------

    buy_probability = 0

    if discount_percentage >= 20:
        buy_probability += random.randint(10, 25)

    if loyalty_score > 70:
        buy_probability += random.randint(10, 20)

    if purchase_frequency > 10:
        buy_probability += random.randint(5, 15)

    if festival == 1:
        buy_probability += random.randint(5, 20)

    if income > 100000:
        buy_probability += random.randint(5, 10)

    if weekend == 1:
        buy_probability += random.randint(0, 10)

    # Random customer behavior
    buy_probability += random.randint(0, 40)

    buy_or_not = 1 if buy_probability > 45 else 0

    # -----------------------------------------------------
    # SALES LOGIC
    # -----------------------------------------------------

    sales_amount = (
        base_price *
        quantity *
        (1 - discount_percentage / 100)
    )

    # Festival sales boost
    if festival == 1:
        sales_amount *= random.uniform(1.1, 1.5)

    # Beverage summer boost
    if category == "Beverages" and season == "Summer":
        sales_amount *= random.uniform(1.1, 1.4)

    # Snacks weekend boost
    if category == "Snacks" and weekend == 1:
        sales_amount *= random.uniform(1.05, 1.3)

    # Add few outliers
    if random.random() < 0.01:
        sales_amount *= random.randint(5, 10)

    sales_amount = round(sales_amount, 2)

    # -----------------------------------------------------
    # PROFIT
    # -----------------------------------------------------

    profit_margin = random.uniform(0.05, 0.4)

    profit = round(
        sales_amount * profit_margin,
        2
    )

    # Some loss-making transactions
    if random.random() < 0.03:
        profit = -abs(profit)

    # -----------------------------------------------------
    # DEMAND SCORE
    # -----------------------------------------------------

    demand_score = round(
        (
            quantity * 0.4 +
            loyalty_score * 0.3 +
            purchase_frequency * 0.3
        ),
        2
    )

    # -----------------------------------------------------
    # APPEND ROW
    # -----------------------------------------------------

    dataset.append([

        customer_id,
        customer_name,
        age,
        gender,
        city,
        state,
        income,

        membership,
        loyalty_score,
        purchase_frequency,
        customer_rating,

        category,
        product_name,
        base_price,
        quantity,
        discount_percentage,

        inventory_level,

        season,
        festival,
        weekend,

        payment_method,

        order_date,

        buy_or_not,

        sales_amount,
        profit,
        demand_score
    ])

# =========================================================
# COLUMN NAMES
# =========================================================

columns = [

    "Customer_ID",
    "Customer_Name",
    "Age",
    "Gender",
    "City",
    "State",
    "Income",

    "Membership_Level",
    "Loyalty_Score",
    "Purchase_Frequency",
    "Customer_Rating",

    "Product_Category",
    "Product_Name",
    "Base_Price",
    "Quantity",
    "Discount_Percentage",

    "Inventory_Level",

    "Season",
    "Festival",
    "Weekend",

    "Payment_Method",

    "Order_Date",

    "Buy_or_Not",

    "Sales_Amount",
    "Profit",
    "Demand_Score"
]

# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame(dataset, columns=columns)

# =========================================================
# REALISTIC MISSING VALUES
# =========================================================

missing_percentages = {

    "Income": 0.07,

    "Membership_Level": 0.04,

    "Customer_Rating": 0.03,

    "Discount_Percentage": 0.02,

    "Inventory_Level": 0.11,

    "Payment_Method": 0.06
}

for column, percentage in missing_percentages.items():

    df.loc[
        df.sample(frac=percentage).index,
        column
    ] = np.nan

# =========================================================
# ADD FEW DUPLICATES
# =========================================================

duplicate_rows = df.sample(500)

df = pd.concat(
    [df, duplicate_rows],
    ignore_index=True
)

# =========================================================
# SHUFFLE DATASET
# =========================================================

df = df.sample(frac=1).reset_index(drop=True)

# =========================================================
# SAVE CSV
# =========================================================

df.to_csv(
    "SalesSphereAI_Realistic_Dataset.csv",
    index=False
)

# =========================================================
# OUTPUT
# =========================================================

print("\n========================================")
print(" REALISTIC DATASET GENERATED SUCCESSFULLY ")
print("========================================\n")

print("Dataset Shape:")
print(df.shape)

print("\nMissing Values:\n")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nFirst 5 Rows:\n")
print(df.head())

print("\nCSV File Saved As:")
print("SalesSphereAI_Realistic_Dataset.csv")
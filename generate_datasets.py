from pathlib import Path
import numpy as np
import pandas as pd

# Reproducible dataset
np.random.seed(42)

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Helper values
# -----------------------------

start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2025-06-30")
all_dates = pd.date_range(start_date, end_date, freq="D")

regions = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]
channels = ["Online", "In-Store", "Mobile App"]
customer_segments = ["Budget", "Regular", "Premium", "Loyal"]
payment_methods = ["Credit Card", "Debit Card", "PayPal", "Gift Card"]

# -----------------------------
# 1. stores.csv
# -----------------------------

stores = pd.DataFrame({
    "store_id": [f"S{i:03d}" for i in range(1, 11)],
    "store_name": [
        "Brookfield Central", "Lakeview Plaza", "Northpoint Market",
        "Desert Ridge", "Westwood Outlet", "Riverbend Shops",
        "Oak Hills", "Metro Square", "Pinecrest", "Bayfront Center"
    ],
    "region": [
        "Northeast", "Midwest", "Northeast", "Southwest", "West",
        "Southeast", "Midwest", "Southeast", "Southwest", "West"
    ],
    "store_type": [
        "Mall", "Shopping Center", "Mall", "Outlet", "Outlet",
        "Shopping Center", "Mall", "Urban", "Shopping Center", "Urban"
    ],
    "open_date": pd.to_datetime([
        "2018-04-15", "2019-08-20", "2020-02-10", "2017-11-01", "2021-06-12",
        "2016-09-05", "2019-03-18", "2022-01-22", "2020-07-14", "2021-10-03"
    ])
})

# A little realistic inconsistency
stores.loc[3, "region"] = "southwest"
stores.loc[7, "store_type"] = "urban"

stores.to_csv(RAW_DIR / "stores.csv", index=False)

# -----------------------------
# 2. products.csv
# -----------------------------

categories = {
    "Electronics": ["Headphones", "Chargers", "Smart Home", "Wearables"],
    "Home": ["Kitchen", "Decor", "Storage", "Bedding"],
    "Apparel": ["Tops", "Bottoms", "Outerwear", "Shoes"],
    "Beauty": ["Skincare", "Haircare", "Fragrance", "Makeup"],
    "Fitness": ["Equipment", "Accessories", "Recovery", "Supplements"]
}

brands = ["Aster", "Northline", "Vera", "Summit", "UrbanNest", "CoreFlex", "Luma", "Everly"]

product_rows = []
product_id = 1

for category, subcats in categories.items():
    for subcat in subcats:
        for _ in range(4):
            base_price = {
                "Electronics": np.random.uniform(35, 220),
                "Home": np.random.uniform(15, 150),
                "Apparel": np.random.uniform(20, 120),
                "Beauty": np.random.uniform(10, 90),
                "Fitness": np.random.uniform(20, 180)
            }[category]

            cost_ratio = np.random.uniform(0.45, 0.75)
            unit_cost = base_price * cost_ratio

            product_rows.append({
                "product_id": f"P{product_id:04d}",
                "product_name": f"{np.random.choice(brands)} {subcat} Item {product_id}",
                "category": category,
                "subcategory": subcat,
                "brand": np.random.choice(brands),
                "list_price": round(base_price, 2),
                "unit_cost": round(unit_cost, 2),
                "supplier_lead_time_days": np.random.randint(5, 25),
                "active_flag": np.random.choice(["Y", "N"], p=[0.92, 0.08])
            })

            product_id += 1

products = pd.DataFrame(product_rows)

# A little realistic messiness
products.loc[5, "category"] = "electronics"
products.loc[14, "category"] = "Home "
products.loc[31, "brand"] = np.nan
products.loc[48, "subcategory"] = "accessories"

products.to_csv(RAW_DIR / "products.csv", index=False)

# -----------------------------
# 3. customers.csv
# -----------------------------

n_customers = 1800

customers = pd.DataFrame({
    "customer_id": [f"C{i:05d}" for i in range(1, n_customers + 1)],
    "signup_date": np.random.choice(pd.date_range("2022-01-01", end_date, freq="D"), n_customers),
    "customer_segment": np.random.choice(customer_segments, n_customers, p=[0.28, 0.42, 0.18, 0.12]),
    "home_region": np.random.choice(regions, n_customers, p=[0.23, 0.21, 0.20, 0.16, 0.20]),
    "preferred_channel": np.random.choice(channels, n_customers, p=[0.48, 0.32, 0.20]),
    "age": np.random.normal(38, 12, n_customers).round().astype(int),
    "email_opt_in": np.random.choice(["Y", "N"], n_customers, p=[0.68, 0.32])
})

customers["age"] = customers["age"].clip(18, 75)

# Missing values and inconsistencies
customers.loc[np.random.choice(customers.index, 45, replace=False), "age"] = np.nan
customers.loc[np.random.choice(customers.index, 35, replace=False), "home_region"] = np.nan
customers.loc[np.random.choice(customers.index, 25, replace=False), "preferred_channel"] = "online"
customers.loc[np.random.choice(customers.index, 20, replace=False), "customer_segment"] = " regular"

# Duplicate rows
duplicate_customers = customers.sample(8, random_state=42)
customers = pd.concat([customers, duplicate_customers], ignore_index=True)

customers.to_csv(RAW_DIR / "customers.csv", index=False)

# -----------------------------
# 4. marketing_campaigns.csv
# -----------------------------

campaign_rows = []
campaign_id = 1

campaign_months = pd.date_range(start_date, end_date, freq="MS")

for month in campaign_months:
    n_campaigns = np.random.choice([1, 2, 3], p=[0.35, 0.45, 0.20])

    for _ in range(n_campaigns):
        campaign_start = month + pd.Timedelta(days=np.random.randint(0, 15))
        campaign_end = campaign_start + pd.Timedelta(days=np.random.randint(10, 35))

        campaign_rows.append({
            "campaign_id": f"M{campaign_id:04d}",
            "campaign_name": f"{np.random.choice(['Spring', 'Summer', 'Holiday', 'Member', 'Flash', 'Clearance'])} Campaign {campaign_id}",
            "start_date": campaign_start,
            "end_date": campaign_end,
            "channel": np.random.choice(["Email", "Social", "Search", "Display", "SMS"], p=[0.32, 0.25, 0.18, 0.15, 0.10]),
            "target_segment": np.random.choice(customer_segments + ["All"], p=[0.20, 0.30, 0.15, 0.10, 0.25]),
            "target_category": np.random.choice(list(categories.keys()) + ["All"], p=[0.18, 0.18, 0.18, 0.16, 0.15, 0.15]),
            "budget": round(np.random.uniform(8000, 65000), 2),
            "planned_discount_pct": round(np.random.choice([0.05, 0.10, 0.15, 0.20, 0.25], p=[0.18, 0.30, 0.28, 0.16, 0.08]), 2)
        })

        campaign_id += 1

marketing_campaigns = pd.DataFrame(campaign_rows)

# Small messiness
marketing_campaigns.loc[np.random.choice(marketing_campaigns.index, 4, replace=False), "budget"] = np.nan
marketing_campaigns.loc[np.random.choice(marketing_campaigns.index, 3, replace=False), "channel"] = "email"

marketing_campaigns.to_csv(RAW_DIR / "marketing_campaigns.csv", index=False)

# -----------------------------
# 5. orders.csv and order_items.csv
# -----------------------------

n_orders = 9500

date_weights = []
for date in all_dates:
    month = date.month

    # Seasonality
    weight = 1.0
    if month in [11, 12]:
        weight *= 1.55
    elif month in [6, 7, 8]:
        weight *= 1.20
    elif month in [1, 2]:
        weight *= 0.82

    # Slight weekday/weekend behavior
    if date.weekday() >= 5:
        weight *= 1.12

    date_weights.append(weight)

date_weights = np.array(date_weights)
date_weights = date_weights / date_weights.sum()

order_dates = np.random.choice(all_dates, size=n_orders, p=date_weights)
order_dates = pd.to_datetime(order_dates)

orders = pd.DataFrame({
    "order_id": [f"O{i:06d}" for i in range(1, n_orders + 1)],
    "customer_id": np.random.choice(customers["customer_id"].unique(), n_orders),
    "store_id": np.random.choice(stores["store_id"], n_orders),
    "order_date": order_dates,
    "sales_channel": np.random.choice(channels, n_orders, p=[0.50, 0.31, 0.19]),
    "payment_method": np.random.choice(payment_methods, n_orders, p=[0.58, 0.22, 0.15, 0.05]),
    "order_status": np.random.choice(["Completed", "Returned", "Cancelled"], n_orders, p=[0.90, 0.06, 0.04]),
})

# Attach campaigns when order date falls inside campaign windows
campaign_lookup = marketing_campaigns.copy()
campaign_ids = []

for _, order in orders.iterrows():
    possible = campaign_lookup[
        (campaign_lookup["start_date"] <= order["order_date"]) &
        (campaign_lookup["end_date"] >= order["order_date"])
    ]

    if len(possible) > 0 and np.random.rand() < 0.42:
        campaign_ids.append(np.random.choice(possible["campaign_id"]))
    else:
        campaign_ids.append(np.nan)

orders["campaign_id"] = campaign_ids

# Shipping details
orders["promised_shipping_days"] = np.where(
    orders["sales_channel"].isin(["Online", "Mobile App"]),
    np.random.choice([2, 3, 4, 5], n_orders, p=[0.25, 0.40, 0.25, 0.10]),
    0
)

orders["actual_shipping_days"] = orders["promised_shipping_days"] + np.random.choice(
    [0, 1, 2, 3, 4],
    n_orders,
    p=[0.58, 0.22, 0.11, 0.06, 0.03]
)

orders.loc[orders["sales_channel"] == "In-Store", "actual_shipping_days"] = 0

# Some missing shipping values for cancelled orders
cancelled_idx = orders[orders["order_status"] == "Cancelled"].index
orders.loc[cancelled_idx, "actual_shipping_days"] = np.nan

# Small messiness
orders.loc[np.random.choice(orders.index, 30, replace=False), "sales_channel"] = "online"
orders.loc[np.random.choice(orders.index, 25, replace=False), "payment_method"] = np.nan

# Duplicate order rows
duplicate_orders = orders.sample(12, random_state=99)
orders = pd.concat([orders, duplicate_orders], ignore_index=True)

# Order items
order_item_rows = []
item_id = 1

product_ids = products["product_id"].values
product_category_map = products.set_index("product_id")["category"].to_dict()
product_price_map = products.set_index("product_id")["list_price"].to_dict()
product_cost_map = products.set_index("product_id")["unit_cost"].to_dict()

campaign_discount_map = marketing_campaigns.set_index("campaign_id")["planned_discount_pct"].to_dict()

for _, order in orders.drop_duplicates("order_id").iterrows():
    if order["order_status"] == "Cancelled":
        n_items = np.random.choice([1, 2], p=[0.75, 0.25])
    else:
        n_items = np.random.choice([1, 2, 3, 4], p=[0.48, 0.31, 0.15, 0.06])

    chosen_products = np.random.choice(product_ids, size=n_items, replace=False)

    for product_id_value in chosen_products:
        list_price = product_price_map[product_id_value]
        unit_cost = product_cost_map[product_id_value]

        quantity = np.random.choice([1, 2, 3, 4], p=[0.66, 0.23, 0.08, 0.03])

        base_discount = np.random.choice([0, 0.05, 0.10, 0.15], p=[0.55, 0.22, 0.16, 0.07])

        if pd.notna(order["campaign_id"]):
            campaign_discount = campaign_discount_map.get(order["campaign_id"], 0)
            discount_pct = max(base_discount, campaign_discount)
        else:
            discount_pct = base_discount

        # Mild time-based variation
        if order["order_date"] >= pd.Timestamp("2025-01-01"):
            if np.random.rand() < 0.25:
                discount_pct = min(discount_pct + np.random.choice([0.05, 0.10]), 0.35)

        unit_price = round(list_price * (1 - discount_pct), 2)

        order_item_rows.append({
            "order_item_id": f"OI{item_id:07d}",
            "order_id": order["order_id"],
            "product_id": product_id_value,
            "quantity": quantity,
            "unit_price": unit_price,
            "unit_cost": round(unit_cost, 2),
            "discount_pct": round(discount_pct, 2)
        })

        item_id += 1

order_items = pd.DataFrame(order_item_rows)

# Messiness
order_items.loc[np.random.choice(order_items.index, 25, replace=False), "discount_pct"] = np.nan
order_items.loc[np.random.choice(order_items.index, 15, replace=False), "unit_cost"] = np.nan

duplicate_items = order_items.sample(15, random_state=123)
order_items = pd.concat([order_items, duplicate_items], ignore_index=True)

orders.to_csv(RAW_DIR / "orders.csv", index=False)
order_items.to_csv(RAW_DIR / "order_items.csv", index=False)

# -----------------------------
# 6. inventory.csv
# -----------------------------

inventory_rows = []
months = pd.date_range(start_date, end_date, freq="MS")

for month in months:
    for store_id in stores["store_id"]:
        for product_id_value in products["product_id"]:
            product_category = product_category_map[product_id_value]

            base_stock = {
                "Electronics": np.random.randint(20, 90),
                "Home": np.random.randint(25, 110),
                "Apparel": np.random.randint(30, 140),
                "Beauty": np.random.randint(20, 100),
                "Fitness": np.random.randint(18, 95),
                "electronics": np.random.randint(20, 90),
                "Home ": np.random.randint(25, 110)
            }.get(product_category, np.random.randint(20, 100))

            seasonal_factor = 1.0
            if month.month in [11, 12]:
                seasonal_factor = 1.35
            elif month.month in [6, 7, 8]:
                seasonal_factor = 1.15

            beginning_inventory = int(base_stock * np.random.uniform(0.65, 1.25))
            restock_qty = int(base_stock * np.random.uniform(0.20, 0.95) * seasonal_factor)
            units_sold_estimate = int(base_stock * np.random.uniform(0.35, 1.10) * seasonal_factor)

            ending_inventory = max(beginning_inventory + restock_qty - units_sold_estimate, 0)

            stockout_days = 0
            if ending_inventory < base_stock * 0.15:
                stockout_days = np.random.choice([1, 2, 3, 4, 5, 6, 7], p=[0.25, 0.22, 0.18, 0.14, 0.10, 0.07, 0.04])

            inventory_rows.append({
                "inventory_month": month,
                "store_id": store_id,
                "product_id": product_id_value,
                "beginning_inventory": beginning_inventory,
                "restock_qty": restock_qty,
                "ending_inventory": ending_inventory,
                "stockout_days": stockout_days,
                "reorder_level": int(base_stock * 0.25)
            })

inventory = pd.DataFrame(inventory_rows)

# Some missing and duplicate inventory records
inventory.loc[np.random.choice(inventory.index, 40, replace=False), "ending_inventory"] = np.nan
inventory.loc[np.random.choice(inventory.index, 30, replace=False), "stockout_days"] = np.nan

duplicate_inventory = inventory.sample(20, random_state=77)
inventory = pd.concat([inventory, duplicate_inventory], ignore_index=True)

inventory.to_csv(RAW_DIR / "inventory.csv", index=False)

# -----------------------------
# Final confirmation
# -----------------------------

print("Datasets created successfully in data/raw/")
print(f"customers.csv: {customers.shape}")
print(f"orders.csv: {orders.shape}")
print(f"order_items.csv: {order_items.shape}")
print(f"products.csv: {products.shape}")
print(f"stores.csv: {stores.shape}")
print(f"inventory.csv: {inventory.shape}")
print(f"marketing_campaigns.csv: {marketing_campaigns.shape}")
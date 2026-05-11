import pandas as pd

df = pd.read_csv("products.csv")

print("Null values count:")
print(df.isnull().sum())

print("\nNull percentage:")
print(df.isnull().mean() * 100)



# fill missing values
df["quantity"] = df["quantity"].fillna(1)
df["price"] = df["price"].fillna(df["price"].median())

# remove duplicates
print("\nDuplicates:", df.duplicated().sum())
df = df.drop_duplicates()


df["revenue"] = df["quantity"] * df["price"]


high_rev = df[df["revenue"] > 5000]
print("\nHigh revenue rows:")
print(high_rev)


product_total = df.groupby("product")["revenue"].sum()
print("\nRevenue by product:")
print(product_total.sort_values(ascending=False))


top5 = df.nlargest(5, "revenue")[["product", "revenue"]]
print("\nTop 5 products:")
print(top5)


df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.month

orders = df["month"].value_counts()
print("\nMonth with highest orders:", orders.idxmax())


df.to_csv("cleaned_data.csv", index=False)

print("\nCleaned data saved successfully")
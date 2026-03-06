import pandas as pd

# 1) Read the three CSVs
df0 = pd.read_csv("data/daily_sales_data_0.csv")
df1 = pd.read_csv("data/daily_sales_data_1.csv")
df2 = pd.read_csv("data/daily_sales_data_2.csv")

# 2) Concatenate into one dataframe
df = pd.concat([df0, df1, df2], ignore_index=True)

# (Recommended) normalize column names + product text so filtering is reliable
df.columns = df.columns.str.strip().str.lower()
df["product"] = df["product"].astype(str).str.strip().str.lower()

# 3) Filter to Pink Morsel only
df = df[df["product"] == "pink morsel"]

# 4) Create Sales = quantity * price  ✅ ensure numeric (no $ formatting)
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
    .astype(float)
)

df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

df["Sales"] = df["quantity"] * df["price"]

# 5) Keep only the required fields (and correct capitalization)
out = df[["Sales", "date", "region"]].copy()
out.columns = ["Sales", "Date", "Region"]

# 6) Save the formatted output file
out.to_csv("data/pink_morsel_sales.csv", index=False)

print("Saved:", "data/pink_morsel_sales.csv")
print(out.head())
print(out.dtypes)   # optional: confirm Sales is numeric
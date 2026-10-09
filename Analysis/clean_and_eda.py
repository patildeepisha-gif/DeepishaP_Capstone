Task 1
import pandas as pd

df = pd.read_csv('orders.csv')
print(df.shape)

Task 2
import pandas as pd
orders = pd.read_csv('orders.csv')
print("Unique values before fix:", orders['payment_method'].unique())
orders['payment_method'] = orders['payment_method'].astype(str).str.strip().str.upper()
print("Unique values after fix:", orders['payment_method'].unique())

Task3
import pandas as pd
orders = pd.read_csv('orders.csv')
dup_cols = ['customer_id', 'product_id', 'order_date', 'quantity', 'discount_pct', 'payment_method', 'rating', 'returned']
orders_clean = orders[~orders.duplicated(subset=dup_cols, keep='first')].copy()
print(orders_clean.shape)
duplicates_mask = orders.duplicated(subset=dup_cols, keep='first')
dropped_orders = orders[duplicates_mask]
print(dropped_orders['order_id'].tolist())

Task4
import pandas as pd
orders = pd.read_csv('orders.csv')

median_rating = orders_clean['rating'].median()
print(median_rating)

orders_clean['discount_pct'] = orders_clean['discount_pct'].fillna(0)
orders_clean['rating'] = orders_clean['rating'].fillna(median_rating)

print("Null counts after imputation:")
print(orders_clean[['discount_pct', 'rating']].isnull().sum().to_dict())

import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_visualizations():
    os.makedirs('visualizations', exist_ok=True)

    
    customers = pd.read_csv('datacustomers.csv')
    orders = pd.read_csv('dataorders.csv')
    products = pd.read_csv('dataproducts.csv')

    orders['payment_method'] = orders['payment_method'].astype(str).str.strip().str.upper()
    dup_cols = ['customer_id', 'product_id', 'order_date', 'quantity', 'discount_pct', 'payment_method', 'rating', 'returned']
    orders_clean = orders[~orders.duplicated(subset=dup_cols, keep='first')].copy()

    median_rating = orders_clean['rating'].median()
    orders_clean['discount_pct'] = orders_clean['discount_pct'].fillna(0)
    orders_clean['rating'] = orders_clean['rating'].fillna(median_rating)

    merged = orders_clean.merge(products, on='product_id', how='left').merge(customers, on='customer_id', how='left')
    merged['order_value'] = merged['quantity'] * merged['price'] * (1 - merged['discount_pct'] / 100.0)

    q1 = merged['quantity'].quantile(0.25)
    q3 = merged['quantity'].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    merged['is_outlier'] = (merged['quantity'] < lower) | (merged['quantity'] > upper)

   
    pm_summary = merged.groupby('payment_method')['returned'].agg(['count', 'mean']).reset_index()
    pm_summary['return_pct'] = pm_summary['mean'] * 100
    pm_summary = pm_summary.sort_values(by='return_pct', ascending=False)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(pm_summary['payment_method'], pm_summary['return_pct'], color=['#d9534f', '#5bc0de', '#4cae4c'], width=0.5)
    
    plt.title("COD Returns at 44.4% — 3x Card", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Payment Method", fontsize=11, labelpad=10)
    plt.ylabel("Return Rate (%)", fontsize=11, labelpad=10)
    plt.ylim(0, 55)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('visualizations/return_rate_by_payment.png', dpi=300)
    plt.show()

   
    merged['order_date'] = pd.to_datetime(merged['order_date'])
    merged['year_month'] = merged['order_date'].dt.to_period('M').astype(str)
    
    ts_clean = merged[~merged['is_outlier']].groupby('year_month')['order_value'].sum().reset_index()

    plt.figure(figsize=(9, 5))
    plt.plot(ts_clean['year_month'], ts_clean['order_value'], marker='o', color='#2b5c8f', linewidth=2.5, markersize=7)
    
    plt.title("Outlier-Corrected Monthly Revenue: March is the Genuine Peak Month", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Month (2026)", fontsize=11, labelpad=10)
    plt.ylabel("Total Revenue (₹)", fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.6)

    for idx, row in ts_clean.iterrows():
        plt.annotate(
            f"₹{row['order_value']:,.2f}", 
            (row['year_month'], row['order_value']),
            textcoords="offset points", 
            xytext=(0, 10), 
            ha='center',
            fontsize=9,
            fontweight='bold' if row['year_month'] == '2026-03' else 'normal'
        )

    plt.tight_layout()
    plt.savefig('visualizations/monthly_revenue_trend.png', dpi=300)
    plt.show()

    print("Visualizations successfully saved to visualizations/ directory.")

if __name__ == '__main__':
    generate_visualizations()

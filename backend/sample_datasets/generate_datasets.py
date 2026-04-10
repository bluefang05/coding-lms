"""
Generate sample datasets for the Pandas Gamified LMS course
These datasets are used in various modules and mini-projects
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_video_games_catalog():
    """Module 1: Video Games Catalog dataset"""
    np.random.seed(42)
    
    games = []
    genres = ['Action', 'RPG', 'Strategy', 'Sports', 'Puzzle', 'Adventure', 'Simulation']
    producers = ['Studio A', 'Studio B', 'Studio C', 'Studio D', 'Indie Dev']
    platforms = ['PC', 'PlayStation', 'Xbox', 'Nintendo Switch', 'Mobile']
    
    for i in range(200):
        game = {
            'id': i + 1,
            'title': f'Game {i + 1}',
            'genre': random.choice(genres),
            'producer': random.choice(producers),
            'platform': random.choice(platforms),
            'release_year': random.randint(2015, 2024),
            'rating': round(np.random.uniform(3.0, 10.0), 1),
            'reviews_count': random.randint(100, 50000),
            'price_usd': round(np.random.uniform(9.99, 69.99), 2),
            'units_sold': random.randint(1000, 5000000)
        }
        games.append(game)
    
    df = pd.DataFrame(games)
    return df

def generate_dirty_sales_data():
    """Module 2: Dirty Sales Data for cleaning practice"""
    np.random.seed(43)
    
    n_records = 500
    dates = [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365)) for _ in range(n_records)]
    
    # Intentionally create messy data
    data = {
        'order_id': list(range(1, n_records + 1)),
        'date': [d.strftime('%Y/%m/%d') if random.random() > 0.1 else d.strftime('%d-%m-%Y') for d in dates],
        'customer_name': [f'Customer {i}' if random.random() > 0.05 else None for i in range(n_records)],
        'product': [random.choice(['Product A', 'Product B', 'Product C', 'Product D']) for _ in range(n_records)],
        'quantity': [random.randint(1, 10) if random.random() > 0.08 else '' for _ in range(n_records)],
        'unit_price': [round(random.uniform(10.0, 100.0), 2) if random.random() > 0.07 else 'N/A' for _ in range(n_records)],
        'total': [],
        'region': [random.choice(['North', 'South', 'East', 'West', 'Central']) for _ in range(n_records)],
        'sales_rep': [f'Rep {random.randint(1, 20)}' for _ in range(n_records)]
    }
    
    # Calculate totals (some will be wrong due to messy quantity/price)
    for i in range(n_records):
        try:
            qty = float(data['quantity'][i]) if data['quantity'][i] != '' else np.nan
            price = float(data['unit_price'][i]) if data['unit_price'][i] != 'N/A' else np.nan
            total = qty * price if not (np.isnan(qty) or np.isnan(price)) else np.nan
            data['total'].append(round(total, 2) if not np.isnan(total) else None)
        except:
            data['total'].append(None)
    
    # Add some duplicates
    duplicate_indices = random.sample(range(n_records), 20)
    for idx in duplicate_indices:
        data['order_id'].append(data['order_id'][idx])
        data['date'].append(data['date'][idx])
        data['customer_name'].append(data['customer_name'][idx])
        data['product'].append(data['product'][idx])
        data['quantity'].append(data['quantity'][idx])
        data['unit_price'].append(data['unit_price'][idx])
        data['total'].append(data['total'][idx])
        data['region'].append(data['region'][idx])
        data['sales_rep'].append(data['sales_rep'][idx])
    
    df = pd.DataFrame(data)
    return df

def generate_survey_data_wide():
    """Module 3: Survey Data in Wide Format for transformation"""
    np.random.seed(44)
    
    respondents = 100
    data = {
        'respondent_id': range(1, respondents + 1),
        'age_group': random.choices(['18-25', '26-35', '36-45', '46-55', '55+'], k=respondents),
        'gender': random.choices(['M', 'F', 'Other'], weights=[0.48, 0.48, 0.04], k=respondents),
        'region': random.choices(['North', 'South', 'East', 'West'], k=respondents),
        'satisfaction_Q1': np.random.randint(1, 6, respondents),
        'satisfaction_Q2': np.random.randint(1, 6, respondents),
        'satisfaction_Q3': np.random.randint(1, 6, respondents),
        'satisfaction_Q4': np.random.randint(1, 6, respondents),
        'likelihood_recommend': np.random.randint(0, 11, respondents),
        'usage_frequency': random.choices(['Daily', 'Weekly', 'Monthly', 'Rarely'], k=respondents)
    }
    
    df = pd.DataFrame(data)
    return df

def generate_sales_transactions():
    """Module 4 & 5: Sales Transactions for aggregation and joins"""
    np.random.seed(45)
    
    n_transactions = 1000
    dates = [datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23)) for _ in range(n_transactions)]
    
    data = {
        'transaction_id': range(1, n_transactions + 1),
        'timestamp': dates,
        'customer_id': np.random.randint(1, 201, n_transactions),
        'product_id': np.random.randint(1, 51, n_transactions),
        'quantity': np.random.randint(1, 10, n_transactions),
        'unit_price': np.round(np.random.uniform(10.0, 200.0, n_transactions), 2),
        'payment_method': random.choices(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet'], k=n_transactions),
        'store_id': np.random.randint(1, 11, n_transactions)
    }
    
    df = pd.DataFrame(data)
    df['total_amount'] = df['quantity'] * df['unit_price']
    return df

def generate_customers():
    """Module 5: Customers table for joins"""
    np.random.seed(46)
    
    n_customers = 200
    data = {
        'customer_id': range(1, n_customers + 1),
        'customer_name': [f'Customer {i}' for i in range(1, n_customers + 1)],
        'email': [f'customer{i}@example.com' for i in range(1, n_customers + 1)],
        'registration_date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1000)) for _ in range(n_customers)],
        'country': random.choices(['USA', 'Canada', 'UK', 'Germany', 'France', 'Spain'], k=n_customers),
        'segment': random.choices(['Premium', 'Standard', 'Budget'], weights=[0.2, 0.5, 0.3], k=n_customers),
        'age': np.random.randint(18, 70, n_customers),
        'gender': random.choices(['M', 'F', 'Other'], weights=[0.48, 0.48, 0.04], k=n_customers)
    }
    
    return pd.DataFrame(data)

def generate_products():
    """Module 5: Products table for joins"""
    np.random.seed(47)
    
    n_products = 50
    categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books', 'Toys']
    
    data = {
        'product_id': range(1, n_products + 1),
        'product_name': [f'Product {i}' for i in range(1, n_products + 1)],
        'category': random.choices(categories, k=n_products),
        'subcategory': [f'Subcategory {random.randint(1, 5)}' for _ in range(n_products)],
        'brand': random.choices(['Brand A', 'Brand B', 'Brand C', 'Brand D', 'Generic'], k=n_products),
        'cost': np.round(np.random.uniform(5.0, 100.0, n_products), 2),
        'weight_kg': np.round(np.random.uniform(0.1, 20.0, n_products), 2),
        'is_active': random.choices([True, False], weights=[0.9, 0.1], k=n_products)
    }
    
    return pd.DataFrame(data)

def generate_time_series_data():
    """Module 6: Time Series Data for temporal analysis"""
    np.random.seed(48)
    
    # Generate hourly data for a year
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(365 * 24)]
    
    # Create realistic patterns
    trend = np.linspace(100, 150, len(dates))
    daily_seasonality = 20 * np.sin(np.linspace(0, 2 * np.pi * 365, len(dates)))
    weekly_seasonality = 10 * np.sin(np.linspace(0, 2 * np.pi * 52, len(dates)))
    noise = np.random.normal(0, 5, len(dates))
    
    values = trend + daily_seasonality + weekly_seasonality + noise
    
    data = {
        'timestamp': dates,
        'value': np.round(values, 2),
        'category': random.choices(['A', 'B', 'C'], k=len(dates)),
        'region': random.choices(['North', 'South'], k=len(dates))
    }
    
    df = pd.DataFrame(data)
    return df

def generate_server_logs():
    """Module 6: Server Logs for time series practice"""
    np.random.seed(49)
    
    n_logs = 5000
    base_time = datetime(2024, 1, 1)
    timestamps = [base_time + timedelta(seconds=random.randint(0, 30 * 24 * 3600)) for _ in range(n_logs)]
    
    endpoints = ['/api/users', '/api/products', '/api/orders', '/api/search', '/health', '/login', '/logout']
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    status_codes = [200, 201, 400, 401, 403, 404, 500]
    
    data = {
        'timestamp': sorted(timestamps),
        'endpoint': random.choices(endpoints, k=n_logs),
        'method': random.choices(methods, weights=[0.6, 0.25, 0.1, 0.05], k=n_logs),
        'status_code': random.choices(status_codes, weights=[0.7, 0.1, 0.05, 0.05, 0.02, 0.05, 0.03], k=n_logs),
        'response_time_ms': np.round(np.random.exponential(100, n_logs), 2),
        'user_id': np.random.randint(1, 1001, n_logs),
        'ip_address': [f'192.168.{random.randint(1, 255)}.{random.randint(1, 255)}' for _ in range(n_logs)]
    }
    
    return pd.DataFrame(data)

def save_all_datasets(output_dir='../../data/datasets'):
    """Save all generated datasets to CSV files"""
    os.makedirs(output_dir, exist_ok=True)
    
    datasets = {
        'video_games_catalog.csv': generate_video_games_catalog(),
        'dirty_sales_data.csv': generate_dirty_sales_data(),
        'survey_data_wide.csv': generate_survey_data_wide(),
        'sales_transactions.csv': generate_sales_transactions(),
        'customers.csv': generate_customers(),
        'products.csv': generate_products(),
        'time_series_data.csv': generate_time_series_data(),
        'server_logs.csv': generate_server_logs()
    }
    
    for filename, df in datasets.items():
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"✅ Saved {filename} with {len(df)} records")
    
    print(f"\n🎉 All datasets saved to {output_dir}")

if __name__ == '__main__':
    save_all_datasets()

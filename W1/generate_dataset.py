import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

def generate_ecommerce_dataset():
    """
    Generate realistic e-commerce dataset with multiple tables:
    1. Customers
    2. Products
    3. Transactions
    4. Marketing campaigns
    5. Support tickets
    """

    # Generate Customers Data
    print("Generating customers data...")
    n_customers = 5000

    customers_data = {
        'customer_id': range(1, n_customers + 1),
        'first_name': [fake.first_name() for _ in range(n_customers)],
        'last_name': [fake.last_name() for _ in range(n_customers)],
        'email': [fake.email() for _ in range(n_customers)],
        'age': np.random.normal(35, 12, n_customers).astype(int),
        'gender': np.random.choice(['M', 'F'], n_customers, p=[0.48, 0.52]),
        'city': [fake.city() for _ in range(n_customers)],
        'state': [fake.state_abbr() for _ in range(n_customers)],
        'registration_date': [fake.date_between(start_date='-3y', end_date='today') for _ in range(n_customers)],
        'customer_segment': np.random.choice(['Premium', 'Regular', 'Budget'], n_customers, p=[0.15, 0.6, 0.25])
    }

    customers_df = pd.DataFrame(customers_data)
    customers_df['age'] = np.clip(customers_df['age'], 18, 80)

    # Generate Products Data
    print("Generating products data...")
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty', 'Toys', 'Automotive']
    n_products = 1000

    products_data = {
        'product_id': range(1, n_products + 1),
        'product_name': [f"{fake.catch_phrase()} {fake.word().title()}" for _ in range(n_products)],
        'category': np.random.choice(categories, n_products),
        'price': np.random.lognormal(3, 0.8, n_products),
        'cost': None,  # Will calculate as percentage of price
        'supplier': [fake.company() for _ in range(n_products)],
        'launch_date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(n_products)]
    }

    products_df = pd.DataFrame(products_data)
    products_df['price'] = np.round(products_df['price'], 2)
    products_df['cost'] = np.round(products_df['price'] * np.random.uniform(0.3, 0.7, n_products), 2)

    # Generate Transactions Data
    print("Generating transactions data...")
    n_transactions = 50000

    # Create seasonal patterns
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)

    transactions_data = []

    for i in range(n_transactions):
        # Random date with seasonal bias
        days_range = (end_date - start_date).days
        random_days = np.random.randint(0, days_range)
        transaction_date = start_date + timedelta(days=random_days)

        # Seasonal multiplier (higher in Nov-Dec)
        month = transaction_date.month
        seasonal_multiplier = 1.5 if month in [11, 12] else 1.0

        # Customer selection with bias towards active customers
        customer_id = np.random.choice(customers_df['customer_id'],
                                     p=np.random.dirichlet(np.ones(n_customers) * 0.1))

        # Product selection
        product_id = np.random.choice(products_df['product_id'])
        product_price = products_df[products_df['product_id'] == product_id]['price'].iloc[0]

        # Quantity with bias towards 1-3 items
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.6, 0.25, 0.1, 0.03, 0.02])

        # Apply discounts sometimes
        discount = np.random.choice([0, 0.05, 0.1, 0.15, 0.2], p=[0.7, 0.1, 0.1, 0.05, 0.05])

        # Payment methods
        payment_method = np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'],
                                        p=[0.5, 0.25, 0.15, 0.1])

        transactions_data.append({
            'transaction_id': i + 1,
            'customer_id': customer_id,
            'product_id': product_id,
            'transaction_date': transaction_date,
            'quantity': quantity,
            'unit_price': product_price,
            'discount': discount,
            'total_amount': round(product_price * quantity * (1 - discount), 2),
            'payment_method': payment_method,
            'shipping_cost': round(np.random.uniform(0, 15), 2) if product_price > 50 else round(np.random.uniform(5, 25), 2)
        })

    transactions_df = pd.DataFrame(transactions_data)

    # Generate Marketing Campaigns Data
    print("Generating marketing campaigns data...")
    campaigns_data = {
        'campaign_id': range(1, 21),
        'campaign_name': [f"{fake.catch_phrase()} Campaign" for _ in range(20)],
        'channel': np.random.choice(['Email', 'Social Media', 'Google Ads', 'TV', 'Radio'], 20),
        'start_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(20)],
        'end_date': None,  # Will calculate
        'budget': np.random.uniform(10000, 100000, 20),
        'target_segment': np.random.choice(['Premium', 'Regular', 'Budget', 'All'], 20, p=[0.2, 0.3, 0.2, 0.3])
    }

    campaigns_df = pd.DataFrame(campaigns_data)
    campaigns_df['budget'] = np.round(campaigns_df['budget'], 2)
    campaigns_df['end_date'] = [start + timedelta(days=np.random.randint(7, 90))
                                for start in campaigns_df['start_date']]

    # Generate Customer Support Tickets
    print("Generating support tickets data...")
    n_tickets = 2000

    ticket_types = ['Product Issue', 'Shipping Delay', 'Refund Request', 'Account Problem', 'General Inquiry']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Open', 'In Progress', 'Resolved', 'Closed']

    tickets_data = {
        'ticket_id': range(1, n_tickets + 1),
        'customer_id': np.random.choice(customers_df['customer_id'], n_tickets),
        'created_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(n_tickets)],
        'ticket_type': np.random.choice(ticket_types, n_tickets),
        'priority': np.random.choice(priorities, n_tickets, p=[0.4, 0.35, 0.2, 0.05]),
        'status': np.random.choice(statuses, n_tickets, p=[0.1, 0.15, 0.35, 0.4]),
        'resolution_time_hours': np.random.exponential(24, n_tickets)  # Average 24 hours
    }

    tickets_df = pd.DataFrame(tickets_data)
    tickets_df['resolution_time_hours'] = np.round(tickets_df['resolution_time_hours'], 1)

    # Add some customer churn data
    print("Adding customer behavior data...")

    # Calculate customer metrics
    customer_metrics = transactions_df.groupby('customer_id').agg({
        'transaction_date': ['min', 'max', 'count'],
        'total_amount': ['sum', 'mean']
    }).round(2)

    customer_metrics.columns = ['first_purchase', 'last_purchase', 'total_transactions', 'total_spent', 'avg_order_value']
    customer_metrics = customer_metrics.reset_index()

    # Calculate days since last purchase
    customer_metrics['days_since_last_purchase'] = (pd.Timestamp(datetime.now().date()) - customer_metrics['last_purchase']).dt.days

    # Determine churn with a realistic distribution (70% active, 30% churned)
    customer_metrics['is_churned'] = np.random.choice([0, 1], size=len(customer_metrics), p=[0.7, 0.3])

    # Merge with customers
    customers_df = customers_df.merge(customer_metrics, on='customer_id', how='left')

    # Save all datasets
    print("Saving datasets...")
    import os
    os.makedirs('dataset', exist_ok=True)
    customers_df.to_csv('dataset/customers.csv', index=False)
    products_df.to_csv('dataset/products.csv', index=False)
    transactions_df.to_csv('dataset/transactions.csv', index=False)
    campaigns_df.to_csv('dataset/marketing_campaigns.csv', index=False)
    tickets_df.to_csv('dataset/support_tickets.csv', index=False)

    print("✅ Dataset generation complete!")
    print(f"📊 Generated files:")
    print(f"   - customers.csv ({len(customers_df):,} records)")
    print(f"   - products.csv ({len(products_df):,} records)")
    print(f"   - transactions.csv ({len(transactions_df):,} records)")
    print(f"   - marketing_campaigns.csv ({len(campaigns_df):,} records)")
    print(f"   - support_tickets.csv ({len(tickets_df):,} records)")

    return customers_df, products_df, transactions_df, campaigns_df, tickets_df

# Generate the datasets
if __name__ == "__main__":
    customers, products, transactions, campaigns, tickets = generate_ecommerce_dataset()

    # Display sample data
    print("\n" + "="*50)
    print("SAMPLE DATA PREVIEW")
    print("="*50)

    print("\n📋 Customers Sample:")
    print(customers.head())

    print("\n📋 Products Sample:")
    print(products.head())

    print("\n📋 Transactions Sample:")
    print(transactions.head())

    print("\n📊 Dataset Summary:")
    print(f"Date Range: {transactions['transaction_date'].min()} to {transactions['transaction_date'].max()}")
    print(f"Total Revenue: ${transactions['total_amount'].sum():,.2f}")
    print(f"Average Order Value: ${transactions['total_amount'].mean():.2f}")
    churn_counts = customers['is_churned'].value_counts()
    active_customers = churn_counts.get(0, 0)
    churned_customers = churn_counts.get(1, 0)
    print(f"Active Customers: {active_customers:,}")
    print(f"Churned Customers: {churned_customers:,}")
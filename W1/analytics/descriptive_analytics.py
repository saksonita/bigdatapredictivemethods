"""
Descriptive Analytics Module
Handles "What Happened?" analysis for the web application
"""

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.utils
from datetime import datetime, timedelta

class DescriptiveAnalytics:
    def __init__(self, data):
        self.customers = data['customers']
        self.products = data['products']
        self.transactions = data['transactions']
        self.support_tickets = data.get('support_tickets', pd.DataFrame())
        self.marketing_campaigns = data.get('marketing_campaigns', pd.DataFrame())
        
        # Convert date columns
        self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        self.customers['registration_date'] = pd.to_datetime(self.customers['registration_date'])
        
        # Ensure required columns exist with proper names
        if 'unit_price' in self.transactions.columns and 'total_amount' not in self.transactions.columns:
            self.transactions['total_amount'] = self.transactions['unit_price'] * self.transactions['quantity'] * (1 - self.transactions.get('discount', 0))
    
    def run_analysis(self):
        """Run complete descriptive analysis"""
        results = {
            'customer_overview': self._customer_overview(),
            'sales_performance': self._sales_performance(),
            'product_analysis': self._product_analysis(),
            'temporal_trends': self._temporal_trends(),
            'customer_segmentation': self._customer_segmentation(),
            'charts': self._generate_charts()
        }
        return results
    
    def _customer_overview(self):
        """Analyze customer demographics and behavior"""
        # Basic demographics
        total_customers = len(self.customers)
        active_customers = len(self.customers[self.customers['is_churned'] == 0])
        churned_customers = len(self.customers[self.customers['is_churned'] == 1])
        churn_rate = (churned_customers / total_customers) * 100
        
        # Age analysis
        avg_age = self.customers['age'].mean()
        age_distribution = self.customers['age'].describe()
        
        # Geographic distribution
        top_cities = dict(self.customers['city'].value_counts().head(10))
        top_states = dict(self.customers['state'].value_counts().head(10))
        
        # Customer segments
        segment_distribution = dict(self.customers['customer_segment'].value_counts())
        
        # Registration trends
        monthly_registrations = dict(self.customers.groupby(
            self.customers['registration_date'].dt.to_period('M')
        ).size())
        
        return {
            'total_customers': total_customers,
            'active_customers': active_customers,
            'churned_customers': churned_customers,
            'churn_rate': round(churn_rate, 2),
            'avg_age': round(avg_age, 1),
            'age_distribution': age_distribution.to_dict(),
            'top_cities': top_cities,
            'top_states': top_states,
            'segment_distribution': segment_distribution,
            'monthly_registrations': {str(k): v for k, v in monthly_registrations.items()}
        }
    
    def _sales_performance(self):
        """Analyze sales and revenue metrics"""
        # Basic sales metrics
        total_revenue = self.transactions['total_amount'].sum()
        total_transactions = len(self.transactions)
        avg_order_value = self.transactions['total_amount'].mean()
        avg_discount = self.transactions['discount'].mean()
        
        # Customer metrics
        unique_customers = self.transactions['customer_id'].nunique()
        transactions_per_customer = total_transactions / unique_customers
        revenue_per_customer = total_revenue / unique_customers
        
        # Time-based analysis
        daily_sales = self.transactions.groupby('transaction_date').agg({
            'total_amount': 'sum',
            'transaction_id': 'count'
        }).round(2)
        
        # Monthly analysis
        monthly_sales = self.transactions.groupby(
            self.transactions['transaction_date'].dt.to_period('M')
        ).agg({
            'total_amount': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).round(2)
        
        # Top products by revenue
        product_revenue = self.transactions.groupby('product_id')['total_amount'].sum().sort_values(ascending=False)
        top_products = dict(product_revenue.head(10))
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_transactions': total_transactions,
            'avg_order_value': round(avg_order_value, 2),
            'avg_discount': round(avg_discount * 100, 2),
            'unique_customers': unique_customers,
            'transactions_per_customer': round(transactions_per_customer, 2),
            'revenue_per_customer': round(revenue_per_customer, 2),
            'daily_sales_avg': round(daily_sales['total_amount'].mean(), 2),
            'monthly_sales': {str(k): {'revenue': float(v['total_amount']), 'transactions': int(v['transaction_id'])} 
                            for k, v in monthly_sales.iterrows()},
            'top_products': top_products
        }
    
    def _product_analysis(self):
        """Analyze product performance and categories"""
        # Product categories
        category_distribution = dict(self.products['category'].value_counts())
        
        # Price analysis
        avg_price = self.products['price'].mean()
        price_distribution = dict(self.products['price'].describe())
        
        # Sales by category
        transaction_products = self.transactions.merge(self.products, on='product_id')
        category_sales = transaction_products.groupby('category').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'transaction_id': 'count'
        }).round(2)
        
        # Top selling products - fix the groupby to handle index properly
        product_sales = transaction_products.groupby('product_id').agg({
            'product_name': 'first',
            'quantity': 'sum',
            'total_amount': 'sum'
        }).sort_values('quantity', ascending=False).head(20)
        
        return {
            'total_products': len(self.products),
            'category_distribution': category_distribution,
            'avg_price': round(avg_price, 2),
            'price_distribution': price_distribution,
            'category_sales': {cat: {'revenue': float(data['total_amount']), 
                                   'quantity': int(data['quantity']),
                                   'transactions': int(data['transaction_id'])} 
                             for cat, data in category_sales.iterrows()},
            'top_selling_products': {row['product_name'][:50]: {'quantity': int(row['quantity']), 
                                                              'revenue': float(row['total_amount'])} 
                                   for idx, row in product_sales.iterrows()}
        }
    
    def _temporal_trends(self):
        """Analyze time-based trends and patterns"""
        # Daily patterns
        self.transactions['day_of_week'] = self.transactions['transaction_date'].dt.day_name()
        self.transactions['hour'] = self.transactions['transaction_date'].dt.hour
        
        daily_patterns = self.transactions.groupby('day_of_week')['total_amount'].agg(['sum', 'count']).round(2)
        hourly_patterns = self.transactions.groupby('hour')['total_amount'].agg(['sum', 'count']).round(2)
        
        # Monthly trends
        monthly_trends = self.transactions.groupby(
            self.transactions['transaction_date'].dt.to_period('M')
        ).agg({
            'total_amount': ['sum', 'mean'],
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).round(2)
        
        # Seasonal analysis
        self.transactions['quarter'] = self.transactions['transaction_date'].dt.quarter
        quarterly_sales = dict(self.transactions.groupby('quarter')['total_amount'].sum())
        
        return {
            'daily_patterns': {day: {'revenue': float(data['sum']), 'transactions': int(data['count'])} 
                             for day, data in daily_patterns.iterrows()},
            'hourly_patterns': {int(hour): {'revenue': float(data['sum']), 'transactions': int(data['count'])} 
                              for hour, data in hourly_patterns.iterrows()},
            'monthly_trends': {str(month): {
                'revenue': float(data[('total_amount', 'sum')]),
                'avg_order_value': float(data[('total_amount', 'mean')]),
                'transactions': int(data[('transaction_id', 'count')]),
                'customers': int(data[('customer_id', 'nunique')])
            } for month, data in monthly_trends.iterrows()},
            'quarterly_sales': quarterly_sales
        }
    
    def _customer_segmentation(self):
        """Analyze customer segments and behavior"""
        # RFM Analysis
        current_date = self.transactions['transaction_date'].max()
        
        rfm_data = self.transactions.groupby('customer_id').agg({
            'transaction_date': lambda x: (current_date - x.max()).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'total_amount': 'sum'  # Monetary
        }).round(2)
        
        rfm_data.columns = ['Recency', 'Frequency', 'Monetary']
        
        # Create RFM scores
        try:
            rfm_data['R_Score'] = pd.qcut(rfm_data['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
            rfm_data['F_Score'] = pd.qcut(rfm_data['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
            rfm_data['M_Score'] = pd.qcut(rfm_data['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
        except Exception:
            # Fallback if quantile cuts fail due to duplicate values
            pass
        
        # Customer value tiers
        customer_transactions = self.transactions.groupby('customer_id').agg({
            'total_amount': 'sum',
            'transaction_id': 'count'
        })
        
        # Define value tiers based on total spending
        try:
            customer_transactions['value_tier'] = pd.qcut(
                customer_transactions['total_amount'], 
                q=4, 
                labels=['Bronze', 'Silver', 'Gold', 'Platinum'],
                duplicates='drop'
            )
            value_tier_distribution = dict(customer_transactions['value_tier'].value_counts())
        except Exception:
            # Fallback if quantile cut fails
            value_tier_distribution = {'Standard': len(customer_transactions)}
        
        return {
            'rfm_summary': {
                'avg_recency': round(rfm_data['Recency'].mean(), 1),
                'avg_frequency': round(rfm_data['Frequency'].mean(), 1),
                'avg_monetary': round(rfm_data['Monetary'].mean(), 2)
            },
            'value_tier_distribution': value_tier_distribution,
            'segment_analysis': dict(self.customers['customer_segment'].value_counts())
        }
    
    def _generate_charts(self):
        """Generate chart data for visualization"""
        charts = {}
        
        # Revenue trend chart
        monthly_revenue = self.transactions.groupby(
            self.transactions['transaction_date'].dt.to_period('M')
        )['total_amount'].sum()
        
        charts['revenue_trend'] = {
            'x': [str(x) for x in monthly_revenue.index],
            'y': monthly_revenue.values.tolist(),
            'type': 'line',
            'title': 'Monthly Revenue Trend'
        }
        
        # Customer segment pie chart
        segment_counts = self.customers['customer_segment'].value_counts()
        charts['customer_segments'] = {
            'labels': segment_counts.index.tolist(),
            'values': segment_counts.values.tolist(),
            'type': 'pie',
            'title': 'Customer Segment Distribution'
        }
        
        # Product category bar chart
        transaction_products = self.transactions.merge(self.products, on='product_id')
        category_revenue = transaction_products.groupby('category')['total_amount'].sum().sort_values(ascending=False)
        
        charts['category_revenue'] = {
            'x': category_revenue.index.tolist(),
            'y': category_revenue.values.tolist(),
            'type': 'bar',
            'title': 'Revenue by Product Category'
        }
        
        return charts
    
    def get_api_data(self):
        """Get data formatted for API responses"""
        return self.run_analysis()
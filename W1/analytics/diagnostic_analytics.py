"""
Diagnostic Analytics Module
Handles "Why Did It Happen?" analysis for the web application
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objs as go

class DiagnosticAnalytics:
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
        """Run complete diagnostic analysis"""
        results = {
            'churn_analysis': self._analyze_churn_factors(),
            'revenue_drivers': self._analyze_revenue_drivers(),
            'customer_behavior': self._analyze_customer_behavior(),
            'product_performance': self._analyze_product_performance(),
            'support_impact': self._analyze_support_impact(),
            'correlations': self._correlation_analysis(),
            'charts': self._generate_charts()
        }
        return results
    
    def _analyze_churn_factors(self):
        """Analyze factors contributing to customer churn"""
        # Use existing customer data which already has calculated metrics
        customer_analysis = self.customers.copy()
        
        # Convert date columns if they're strings
        if 'last_purchase' in customer_analysis.columns:
            customer_analysis['last_purchase'] = pd.to_datetime(customer_analysis['last_purchase'])
        if 'first_purchase' in customer_analysis.columns:
            customer_analysis['first_purchase'] = pd.to_datetime(customer_analysis['first_purchase'])
        
        # Use existing days_since_last_purchase or calculate if missing
        if 'days_since_last_purchase' in customer_analysis.columns:
            customer_analysis['days_since_last'] = customer_analysis['days_since_last_purchase']
        elif 'last_purchase' in customer_analysis.columns:
            current_date = self.transactions['transaction_date'].max()
            customer_analysis['days_since_last'] = (current_date - customer_analysis['last_purchase']).dt.days
            customer_analysis['days_since_last'] = customer_analysis['days_since_last'].fillna(365)
        else:
            customer_analysis['days_since_last'] = 0
        
        # Churn analysis by different factors
        churn_by_segment = customer_analysis.groupby('customer_segment')['is_churned'].agg(['count', 'sum', 'mean']).round(3)
        churn_by_age_group = customer_analysis.groupby(pd.cut(customer_analysis['age'], bins=5))['is_churned'].mean().round(3)
        
        # Statistical tests
        # Chi-square test for categorical variables
        from scipy.stats import chi2_contingency
        
        contingency_segment = pd.crosstab(customer_analysis['customer_segment'], customer_analysis['is_churned'])
        chi2_segment, p_segment = chi2_contingency(contingency_segment)[:2]
        
        # T-test for continuous variables
        churned = customer_analysis[customer_analysis['is_churned'] == 1]['total_spent']
        not_churned = customer_analysis[customer_analysis['is_churned'] == 0]['total_spent']
        
        t_stat_spending, p_spending = stats.ttest_ind(churned.dropna(), not_churned.dropna())
        
        return {
            'churn_by_segment': {idx: {'count': int(row['count']), 'churned': int(row['sum']), 'rate': float(row['mean'])} 
                               for idx, row in churn_by_segment.iterrows()},
            'churn_by_age_group': {str(idx): float(rate) for idx, rate in churn_by_age_group.items()},
            'statistical_tests': {
                'segment_churn_chi2': {'statistic': float(chi2_segment), 'p_value': float(p_segment)},
                'spending_churn_ttest': {'statistic': float(t_stat_spending), 'p_value': float(p_spending)}
            },
            'key_insights': [
                f"Segment with highest churn: {churn_by_segment['mean'].idxmax()} ({churn_by_segment['mean'].max():.1%})",
                f"Average spending difference: ${not_churned.mean():.2f} (retained) vs ${churned.mean():.2f} (churned)",
                f"Statistical significance: {'Significant' if p_segment < 0.05 else 'Not significant'} relationship between segment and churn"
            ]
        }
    
    def _analyze_revenue_drivers(self):
        """Analyze what drives revenue performance"""
        # Product performance analysis
        product_revenue = self.transactions.merge(self.products, on='product_id')
        
        # Revenue by category
        category_performance = product_revenue.groupby('category').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'discount': 'mean',
            'quantity': 'sum'
        }).round(2)
        
        # Price elasticity approximation
        price_revenue = product_revenue.groupby('product_id').agg({
            'price': 'first',
            'total_amount': 'sum',
            'quantity': 'sum'
        })
        
        price_revenue_corr = price_revenue['price'].corr(price_revenue['quantity'])
        
        # Customer value analysis
        customer_value = self.transactions.groupby('customer_id').agg({
            'total_amount': 'sum'
        })
        
        # Top 20% vs bottom 20% customers
        top_20_threshold = customer_value['total_amount'].quantile(0.8)
        bottom_20_threshold = customer_value['total_amount'].quantile(0.2)
        
        top_customers = len(customer_value[customer_value['total_amount'] >= top_20_threshold])
        bottom_customers = len(customer_value[customer_value['total_amount'] <= bottom_20_threshold])
        
        top_revenue_share = customer_value[customer_value['total_amount'] >= top_20_threshold]['total_amount'].sum() / customer_value['total_amount'].sum()
        
        return {
            'category_performance': {cat: {
                'revenue': float(data[('total_amount', 'sum')]),
                'avg_order': float(data[('total_amount', 'mean')]),
                'transactions': int(data[('total_amount', 'count')]),
                'avg_discount': float(data[('discount', 'mean')])
            } for cat, data in category_performance.iterrows()},
            'price_quantity_correlation': float(price_revenue_corr),
            'customer_concentration': {
                'top_20_percent_customers': top_customers,
                'top_20_percent_revenue_share': float(top_revenue_share),
                'pareto_principle': f"Top 20% customers generate {top_revenue_share:.1%} of revenue"
            }
        }
    
    def _analyze_customer_behavior(self):
        """Analyze customer purchasing behavior patterns"""
        # Purchase frequency analysis
        customer_frequency = self.transactions.groupby('customer_id').agg({
            'transaction_date': ['count', lambda x: (x.max() - x.min()).days]
        })
        customer_frequency.columns = ['purchase_count', 'customer_lifetime_days']
        customer_frequency['purchase_frequency'] = customer_frequency['purchase_count'] / (customer_frequency['customer_lifetime_days'] + 1)
        
        # Seasonal behavior
        self.transactions['month'] = self.transactions['transaction_date'].dt.month
        self.transactions['quarter'] = self.transactions['transaction_date'].dt.quarter
        
        monthly_patterns = self.transactions.groupby('month')['total_amount'].agg(['sum', 'count']).round(2)
        quarterly_patterns = self.transactions.groupby('quarter')['total_amount'].agg(['sum', 'count']).round(2)
        
        # Day of week patterns
        self.transactions['day_of_week'] = self.transactions['transaction_date'].dt.day_name()
        dow_patterns = self.transactions.groupby('day_of_week')['total_amount'].agg(['sum', 'count']).round(2)
        
        # Discount sensitivity
        discount_bins = [0, 0.05, 0.1, 0.2, 1.0]
        discount_labels = ['No Discount', 'Low (0-5%)', 'Medium (5-10%)', 'High (10%+)']
        self.transactions['discount_category'] = pd.cut(self.transactions['discount'], bins=discount_bins, labels=discount_labels)
        
        discount_response = self.transactions.groupby('discount_category').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'mean'
        }).round(2)
        
        return {
            'purchase_frequency': {
                'avg_purchases_per_customer': float(customer_frequency['purchase_count'].mean()),
                'avg_customer_lifetime_days': float(customer_frequency['customer_lifetime_days'].mean()),
                'avg_purchase_frequency': float(customer_frequency['purchase_frequency'].mean())
            },
            'seasonal_patterns': {
                'monthly': {int(month): {'revenue': float(data['sum']), 'transactions': int(data['count'])} 
                          for month, data in monthly_patterns.iterrows()},
                'quarterly': {int(quarter): {'revenue': float(data['sum']), 'transactions': int(data['count'])} 
                            for quarter, data in quarterly_patterns.iterrows()},
                'day_of_week': {day: {'revenue': float(data['sum']), 'transactions': int(data['count'])} 
                              for day, data in dow_patterns.iterrows()}
            },
            'discount_sensitivity': {str(cat): {
                'revenue': float(data[('total_amount', 'sum')]),
                'avg_order': float(data[('total_amount', 'mean')]),
                'transactions': int(data[('total_amount', 'count')]),
                'avg_quantity': float(data[('quantity', 'mean')])
            } for cat, data in discount_response.iterrows() if pd.notna(cat)}
        }
    
    def _analyze_product_performance(self):
        """Analyze product performance drivers"""
        product_analysis = self.transactions.merge(self.products, on='product_id')
        
        # Performance by price range
        price_bins = [0, 25, 50, 100, float('inf')]
        price_labels = ['Budget (<$25)', 'Mid-range ($25-50)', 'Premium ($50-100)', 'Luxury ($100+)']
        product_analysis['price_category'] = pd.cut(product_analysis['price'], bins=price_bins, labels=price_labels)
        
        price_performance = product_analysis.groupby('price_category').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'discount': 'mean'
        }).round(2)
        
        # Category performance correlation with features
        category_features = product_analysis.groupby('category').agg({
            'price': 'mean',
            'total_amount': 'sum',
            'quantity': 'sum',
            'discount': 'mean'
        })
        
        price_revenue_corr = category_features['price'].corr(category_features['total_amount'])
        
        return {
            'price_performance': {str(cat): {
                'revenue': float(data[('total_amount', 'sum')]),
                'avg_order': float(data[('total_amount', 'mean')]),
                'transactions': int(data[('total_amount', 'count')]),
                'total_quantity': int(data[('quantity', 'sum')]),
                'avg_discount': float(data[('discount', 'mean')])
            } for cat, data in price_performance.iterrows() if pd.notna(cat)},
            'category_insights': {
                'price_revenue_correlation': float(price_revenue_corr),
                'top_revenue_category': category_features['total_amount'].idxmax(),
                'highest_avg_price_category': category_features['price'].idxmax()
            }
        }
    
    def _analyze_support_impact(self):
        """Analyze customer support impact on retention and satisfaction"""
        if len(self.support_tickets) == 0:
            return {'message': 'No support ticket data available'}
        
        # Ticket analysis by customer
        ticket_summary = self.support_tickets.groupby('customer_id').agg({
            'ticket_id': 'count',
            'resolution_time_hours': 'mean',
            'priority': lambda x: (x.isin(['High', 'Critical'])).sum()
        })
        ticket_summary.columns = ['ticket_count', 'avg_resolution_time', 'high_priority_tickets']
        
        # Merge with customer churn data
        customer_support = self.customers.merge(ticket_summary, on='customer_id', how='left')
        customer_support = customer_support.fillna(0)
        
        # Support impact on churn
        support_churn = customer_support.groupby('ticket_count')['is_churned'].mean()
        
        # Resolution time impact
        resolution_bins = [0, 24, 48, 72, float('inf')]
        resolution_labels = ['Quick (<24h)', 'Fast (24-48h)', 'Slow (48-72h)', 'Very Slow (>72h)']
        
        customer_support['resolution_category'] = pd.cut(
            customer_support['avg_resolution_time'], 
            bins=resolution_bins, 
            labels=resolution_labels
        )
        
        resolution_churn = customer_support.groupby('resolution_category')['is_churned'].mean()
        
        return {
            'ticket_impact': {
                'avg_tickets_per_customer': float(ticket_summary['ticket_count'].mean()),
                'avg_resolution_time': float(ticket_summary['avg_resolution_time'].mean()),
                'churn_by_ticket_count': {int(k): float(v) for k, v in support_churn.items()},
                'churn_by_resolution_time': {str(k): float(v) for k, v in resolution_churn.items() if pd.notna(k)}
            }
        }
    
    def _correlation_analysis(self):
        """Analyze correlations between key business metrics"""
        # Use existing customer data which already has calculated metrics
        customer_analysis = self.customers.copy()
        
        # Select only numeric columns that exist in the customer data
        available_numeric_cols = []
        for col in ['age', 'total_spent', 'days_since_last_purchase', 'purchase_frequency', 'is_churned']:
            if col in customer_analysis.columns:
                available_numeric_cols.append(col)
        
        if len(available_numeric_cols) < 3:
            # Fallback: calculate basic metrics if needed
            customer_metrics = self.transactions.groupby('customer_id').agg({
                'total_amount': 'sum',
                'transaction_id': 'count'
            })
            customer_metrics.columns = ['total_spent', 'transaction_count']
            
            customer_analysis = self.customers[['customer_id', 'age', 'is_churned']].merge(customer_metrics, on='customer_id', how='left')
            customer_analysis = customer_analysis.fillna(0)
            available_numeric_cols = ['age', 'total_spent', 'transaction_count', 'is_churned']
        
        # Calculate correlations only for available columns
        correlation_matrix = customer_analysis[available_numeric_cols].corr()
        
        # Key correlations (only calculate if columns exist)
        key_correlations = {}
        if 'age' in available_numeric_cols and 'total_spent' in available_numeric_cols:
            key_correlations['age_spending'] = float(correlation_matrix.loc['age', 'total_spent'])
        if 'total_spent' in available_numeric_cols and 'is_churned' in available_numeric_cols:
            key_correlations['spending_churn'] = float(correlation_matrix.loc['total_spent', 'is_churned'])
        if 'transaction_count' in available_numeric_cols and 'total_spent' in available_numeric_cols:
            key_correlations['frequency_spending'] = float(correlation_matrix.loc['transaction_count', 'total_spent'])
        
        # Create insights based on available correlations
        insights = []
        for key, value in key_correlations.items():
            insights.append(f"{key.replace('_', '-').title()}: {value:.3f}")
        
        return {
            'correlation_matrix': correlation_matrix.round(3).to_dict(),
            'key_correlations': key_correlations,
            'insights': insights
        }
    
    def _generate_charts(self):
        """Generate chart data for diagnostic visualization"""
        charts = {}
        
        # Churn analysis chart
        customer_summary = self.transactions.groupby('customer_id').agg({
            'total_amount': 'sum'
        })
        customer_churn = self.customers.merge(customer_summary, on='customer_id', how='left')
        customer_churn = customer_churn.fillna(0)
        
        churn_by_segment = customer_churn.groupby('customer_segment')['is_churned'].mean()
        
        charts['churn_by_segment'] = {
            'x': churn_by_segment.index.tolist(),
            'y': churn_by_segment.values.tolist(),
            'type': 'bar',
            'title': 'Churn Rate by Customer Segment'
        }
        
        return charts
    
    def get_api_data(self):
        """Get data formatted for API responses"""
        return self.run_analysis()
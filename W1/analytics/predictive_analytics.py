"""
Predictive Analytics Module
Handles "What Will Happen?" analysis for the web application
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class PredictiveAnalytics:
    def __init__(self, data):
        self.customers = data['customers']
        self.products = data['products']
        self.transactions = data['transactions']
        self.support_tickets = data.get('support_tickets', pd.DataFrame())
        
        # Convert date columns
        self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        self.customers['registration_date'] = pd.to_datetime(self.customers['registration_date'])
        
        # Ensure required columns exist with proper names
        if 'unit_price' in self.transactions.columns and 'total_amount' not in self.transactions.columns:
            self.transactions['total_amount'] = self.transactions['unit_price'] * self.transactions['quantity'] * (1 - self.transactions.get('discount', 0))
        
        # Initialize models
        self.churn_model = None
        self.clv_model = None
        self.scaler = StandardScaler()
    
    def run_analysis(self):
        """Run complete predictive analysis"""
        # Prepare features
        customer_features = self._prepare_features()
        
        results = {
            'churn_prediction': self._predict_churn(customer_features),
            'clv_prediction': self._predict_clv(customer_features),
            'sales_forecast': self._forecast_sales(),
            'demand_forecast': self._forecast_demand(),
            'model_performance': self._get_model_performance(),
            'risk_analysis': self._analyze_risks(customer_features),
            'charts': self._generate_charts(customer_features)
        }
        return results
    
    def _prepare_features(self):
        """Prepare features for machine learning models"""
        # Customer transaction features
        customer_features = self.transactions.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'std', 'count'],
            'quantity': ['sum', 'mean'],
            'discount': 'mean',
            'transaction_date': ['min', 'max']
        }).round(2)
        
        # Flatten column names
        customer_features.columns = ['total_spent', 'avg_order_value', 'order_value_std', 'transaction_count',
                                   'total_quantity', 'avg_quantity', 'avg_discount', 'first_purchase', 'last_purchase']
        
        # Calculate additional features
        customer_features['days_active'] = (customer_features['last_purchase'] - customer_features['first_purchase']).dt.days
        customer_features['days_since_last'] = (self.transactions['transaction_date'].max() - customer_features['last_purchase']).dt.days
        customer_features['purchase_frequency'] = customer_features['transaction_count'] / (customer_features['days_active'] + 1)
        customer_features['order_value_std'] = customer_features['order_value_std'].fillna(0)
        
        # Customer support features
        if len(self.support_tickets) > 0:
            support_features = self.support_tickets.groupby('customer_id').agg({
                'ticket_id': 'count',
                'resolution_time_hours': 'mean',
                'priority': lambda x: (x.isin(['High', 'Critical'])).sum()
            }).round(2)
            support_features.columns = ['support_tickets', 'avg_resolution_time', 'high_priority_tickets']
        else:
            support_features = pd.DataFrame(index=customer_features.index)
            support_features['support_tickets'] = 0
            support_features['avg_resolution_time'] = 0
            support_features['high_priority_tickets'] = 0
        
        # Merge all features
        customers_ml = self.customers[['customer_id', 'age', 'gender', 'customer_segment', 'is_churned']].copy()
        customers_ml = customers_ml.merge(customer_features, on='customer_id', how='left')
        customers_ml = customers_ml.merge(support_features, on='customer_id', how='left')
        customers_ml = customers_ml.fillna(0)
        
        # Encode categorical variables
        le_gender = LabelEncoder()
        le_segment = LabelEncoder()
        customers_ml['gender_encoded'] = le_gender.fit_transform(customers_ml['gender'])
        customers_ml['segment_encoded'] = le_segment.fit_transform(customers_ml['customer_segment'])
        
        return customers_ml
    
    def _predict_churn(self, customer_features):
        """Build and train churn prediction model"""
        churn_features = ['age', 'total_spent', 'avg_order_value', 'transaction_count', 
                         'purchase_frequency', 'avg_discount', 'days_since_last',
                         'support_tickets', 'avg_resolution_time', 'high_priority_tickets',
                         'gender_encoded', 'segment_encoded']
        
        # Prepare data
        X = customer_features[churn_features].fillna(0)
        y = customer_features['is_churned']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Train Random Forest model
        self.churn_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.churn_model.fit(X_train, y_train)
        
        # Predictions
        y_pred = self.churn_model.predict(X_test)
        y_proba = self.churn_model.predict_proba(X_test)[:, 1]
        
        # Model performance
        accuracy = accuracy_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': churn_features,
            'importance': self.churn_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Predict for all customers
        customer_features['churn_probability'] = self.churn_model.predict_proba(X)[:, 1]
        
        # High-risk customers
        high_risk_customers = customer_features[customer_features['churn_probability'] > 0.7]
        
        return {
            'model_accuracy': float(accuracy),
            'feature_importance': feature_importance.head(10).to_dict('records'),
            'high_risk_customers': {
                'count': len(high_risk_customers),
                'avg_churn_probability': float(high_risk_customers['churn_probability'].mean()) if len(high_risk_customers) > 0 else 0,
                'total_value_at_risk': float(high_risk_customers['total_spent'].sum()) if len(high_risk_customers) > 0 else 0
            },
            'predictions_summary': {
                'total_customers': len(customer_features),
                'predicted_churners': int((customer_features['churn_probability'] > 0.5).sum()),
                'avg_churn_probability': float(customer_features['churn_probability'].mean())
            }
        }
    
    def _predict_clv(self, customer_features):
        """Build and train Customer Lifetime Value prediction model"""
        # Filter active customers
        active_customers = customer_features[customer_features['is_churned'] == 0].copy()
        
        if len(active_customers) == 0:
            return {'message': 'No active customers for CLV prediction'}
        
        clv_features = ['age', 'transaction_count', 'avg_order_value', 'purchase_frequency',
                       'days_active', 'avg_discount', 'gender_encoded', 'segment_encoded']
        
        # Prepare CLV data
        X_clv = active_customers[clv_features].fillna(0)
        y_clv = active_customers['total_spent']
        
        # Split data
        X_train_clv, X_test_clv, y_train_clv, y_test_clv = train_test_split(X_clv, y_clv, test_size=0.2, random_state=42)
        
        # Train CLV model
        self.clv_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
        self.clv_model.fit(X_train_clv, y_train_clv)
        
        # Predictions
        clv_pred = self.clv_model.predict(X_test_clv)
        
        # Model performance
        r2 = r2_score(y_test_clv, clv_pred)
        rmse = np.sqrt(mean_squared_error(y_test_clv, clv_pred))
        
        # Predict future CLV for all active customers
        active_customers['predicted_clv'] = self.clv_model.predict(X_clv)
        active_customers['clv_segment'] = pd.qcut(active_customers['predicted_clv'], 
                                                 q=4, labels=['Low', 'Medium', 'High', 'Premium'],
                                                 duplicates='drop')
        
        # CLV segmentation
        clv_segments = active_customers.groupby('clv_segment').agg({
            'customer_id': 'count',
            'predicted_clv': 'mean',
            'total_spent': 'mean'
        }).round(2)
        
        return {
            'model_performance': {
                'r2_score': float(r2),
                'rmse': float(rmse)
            },
            'clv_segments': {str(seg): {
                'customer_count': int(data['customer_id']),
                'predicted_clv': float(data['predicted_clv']),
                'current_spent': float(data['total_spent'])
            } for seg, data in clv_segments.iterrows()},
            'predictions_summary': {
                'total_active_customers': len(active_customers),
                'avg_predicted_clv': float(active_customers['predicted_clv'].mean()),
                'total_clv_potential': float(active_customers['predicted_clv'].sum())
            }
        }
    
    def _forecast_sales(self):
        """Forecast future sales trends"""
        # Prepare time series data
        daily_sales = self.transactions.groupby('transaction_date').agg({
            'total_amount': 'sum',
            'transaction_id': 'count',
            'customer_id': 'nunique'
        }).round(2)
        
        daily_sales.columns = ['daily_revenue', 'daily_orders', 'daily_customers']
        
        # Simple trend analysis (last 30 days)
        recent_sales = daily_sales.tail(30)
        
        # Calculate growth rate
        if len(recent_sales) >= 7:
            recent_avg = recent_sales['daily_revenue'].tail(7).mean()
            previous_avg = recent_sales['daily_revenue'].head(7).mean()
            growth_rate = (recent_avg - previous_avg) / previous_avg if previous_avg > 0 else 0
        else:
            growth_rate = 0
        
        # Simple forecast for next 7 days
        last_revenue = daily_sales['daily_revenue'].tail(7).mean()
        forecast_values = []
        
        for i in range(7):
            forecasted_value = last_revenue * (1 + growth_rate) ** (i + 1)
            forecast_values.append(float(forecasted_value))
        
        return {
            'recent_performance': {
                'avg_daily_revenue': float(recent_sales['daily_revenue'].mean()),
                'avg_daily_orders': float(recent_sales['daily_orders'].mean()),
                'growth_rate': float(growth_rate) * 100
            },
            'next_7_days_forecast': forecast_values,
            'forecast_total': float(sum(forecast_values))
        }
    
    def _forecast_demand(self):
        """Forecast product demand"""
        # Analyze top products for demand forecasting
        product_demand = self.transactions.groupby('product_id').agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'transaction_id': 'count'
        }).sort_values('quantity', ascending=False).head(20)
        
        # Merge with product info
        top_products = self.products.merge(product_demand, on='product_id')
        
        # Calculate max quantity for demand score normalization
        max_quantity = top_products['quantity'].max() if len(top_products) > 0 else 1
        
        # Category demand patterns
        category_demand = self.transactions.merge(self.products, on='product_id').groupby('category').agg({
            'quantity': 'sum',
            'total_amount': 'sum'
        }).sort_values('quantity', ascending=False)
        
        return {
            'top_products_demand': {
                str(row['product_id']): {
                    'product_name': row['product_name'],
                    'category': row['category'],
                    'total_quantity': int(row['quantity']),
                    'total_revenue': float(row['total_amount']),
                    'demand_score': float(row['quantity'] / max_quantity)
                } for _, row in top_products.iterrows()
            },
            'category_demand': {
                cat: {
                    'total_quantity': int(data['quantity']),
                    'total_revenue': float(data['total_amount'])
                } for cat, data in category_demand.iterrows()
            }
        }
    
    def _get_model_performance(self):
        """Get model performance metrics"""
        performance = {}
        
        if self.churn_model is not None:
            performance['churn_model'] = {
                'model_type': 'Random Forest Classifier',
                'features_used': 12,
                'training_status': 'Trained'
            }
        
        if self.clv_model is not None:
            performance['clv_model'] = {
                'model_type': 'Random Forest Regressor',
                'features_used': 8,
                'training_status': 'Trained'
            }
        
        return performance
    
    def _analyze_risks(self, customer_features):
        """Analyze business risks based on predictions"""
        if 'churn_probability' not in customer_features.columns:
            return {'message': 'Churn predictions not available'}
        
        # Risk segmentation
        customer_features['risk_segment'] = pd.cut(
            customer_features['churn_probability'],
            bins=[0, 0.3, 0.6, 1.0],
            labels=['Low Risk', 'Medium Risk', 'High Risk']
        )
        
        risk_analysis = customer_features.groupby('risk_segment').agg({
            'customer_id': 'count',
            'total_spent': ['sum', 'mean'],
            'churn_probability': 'mean'
        }).round(3)
        
        # High-value at-risk customers
        high_value_threshold = customer_features['total_spent'].quantile(0.75)
        high_value_at_risk = customer_features[
            (customer_features['churn_probability'] > 0.7) & 
            (customer_features['total_spent'] > high_value_threshold)
        ]
        
        return {
            'risk_segmentation': {
                str(seg): {
                    'customer_count': int(data['customer_id']),
                    'total_value': float(data[('total_spent', 'sum')]),
                    'avg_value': float(data[('total_spent', 'mean')]),
                    'avg_churn_prob': float(data['churn_probability'])
                } for seg, data in risk_analysis.iterrows()
            },
            'high_value_at_risk': {
                'count': len(high_value_at_risk),
                'total_value': float(high_value_at_risk['total_spent'].sum()),
                'avg_churn_probability': float(high_value_at_risk['churn_probability'].mean()) if len(high_value_at_risk) > 0 else 0
            }
        }
    
    def _generate_charts(self, customer_features):
        """Generate chart data for predictive visualization"""
        charts = {}
        
        # Churn probability distribution
        if 'churn_probability' in customer_features.columns:
            churn_hist, bin_edges = np.histogram(customer_features['churn_probability'], bins=20)
            charts['churn_distribution'] = {
                'x': bin_edges[:-1].tolist(),
                'y': churn_hist.tolist(),
                'type': 'histogram',
                'title': 'Churn Probability Distribution'
            }
        
        # Sales forecast chart
        sales_forecast = self._forecast_sales()
        charts['sales_forecast'] = {
            'x': list(range(1, 8)),
            'y': sales_forecast['next_7_days_forecast'],
            'type': 'line',
            'title': 'Next 7 Days Sales Forecast'
        }
        
        return charts
    
    def get_api_data(self):
        """Get data formatted for API responses"""
        return self.run_analysis()
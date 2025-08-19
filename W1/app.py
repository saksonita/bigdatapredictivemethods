"""
E-commerce Analytics Dashboard
A comprehensive Flask web application for descriptive, diagnostic, predictive, and prescriptive analytics
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import plotly.graph_objs as go
import plotly.utils

# Import custom analytics modules
from analytics.descriptive_analytics import DescriptiveAnalytics
from analytics.diagnostic_analytics import DiagnosticAnalytics
from analytics.predictive_analytics import PredictiveAnalytics
from analytics.prescriptive_analytics import PrescriptiveAnalytics

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global variables for cached data
cached_data = {}

def load_data():
    """Load and cache data files"""
    try:
        data = {
            'customers': pd.read_csv('dataset/customers.csv'),
            'products': pd.read_csv('dataset/products.csv'),
            'transactions': pd.read_csv('dataset/transactions.csv')
        }
        
        # Load optional files if they exist
        try:
            data['support_tickets'] = pd.read_csv('dataset/support_tickets.csv')
        except FileNotFoundError:
            print("Warning: support_tickets.csv not found, creating empty DataFrame")
            data['support_tickets'] = pd.DataFrame()
            
        try:
            data['marketing_campaigns'] = pd.read_csv('dataset/marketing_campaigns.csv')
        except FileNotFoundError:
            print("Warning: marketing_campaigns.csv not found, creating empty DataFrame")
            data['marketing_campaigns'] = pd.DataFrame()
        
        # Load analysis results if they exist
        try:
            with open('descriptive_summary.json', 'r') as f:
                data['descriptive_summary'] = json.load(f)
        except FileNotFoundError:
            data['descriptive_summary'] = {}
            
        try:
            with open('diagnostic_insights.json', 'r') as f:
                data['diagnostic_insights'] = json.load(f)
        except FileNotFoundError:
            data['diagnostic_insights'] = {}
            
        try:
            with open('predictions_summary.json', 'r') as f:
                data['predictions_summary'] = json.load(f)
        except FileNotFoundError:
            data['predictions_summary'] = {}
            
        try:
            with open('prescriptive_recommendations.json', 'r') as f:
                data['prescriptive_recommendations'] = json.load(f)
        except FileNotFoundError:
            data['prescriptive_recommendations'] = {}
            
        try:
            data['customer_predictions'] = pd.read_csv('customer_predictions.csv')
        except FileNotFoundError:
            data['customer_predictions'] = pd.DataFrame()
        
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

@app.route('/')
def index():
    """Main dashboard homepage"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    if not cached_data:
        return render_template('error.html', message="Unable to load data files")
    
    # Calculate summary statistics for homepage
    summary_stats = {
        'total_customers': len(cached_data['customers']),
        'total_transactions': len(cached_data['transactions']),
        'total_revenue': cached_data['transactions']['total_amount'].sum(),
        'avg_order_value': cached_data['transactions']['total_amount'].mean(),
        'unique_products': len(cached_data['products']),
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render_template('index.html', stats=summary_stats)

@app.route('/descriptive')
def descriptive():
    """Descriptive Analytics Dashboard"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        desc_analytics = DescriptiveAnalytics(cached_data)
        analysis_results = desc_analytics.run_analysis()
        
        return render_template('descriptive.html', 
                             results=analysis_results,
                             summary=cached_data.get('descriptive_summary', {}))
    except Exception as e:
        return render_template('error.html', message=f"Descriptive analytics error: {e}")

@app.route('/diagnostic')
def diagnostic():
    """Diagnostic Analytics Dashboard"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        diag_analytics = DiagnosticAnalytics(cached_data)
        analysis_results = diag_analytics.run_analysis()
        
        return render_template('diagnostic.html', 
                             results=analysis_results,
                             insights=cached_data.get('diagnostic_insights', {}))
    except Exception as e:
        return render_template('error.html', message=f"Diagnostic analytics error: {e}")

@app.route('/predictive')
def predictive():
    """Predictive Analytics Dashboard"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        pred_analytics = PredictiveAnalytics(cached_data)
        analysis_results = pred_analytics.run_analysis()
        
        return render_template('predictive.html', 
                             results=analysis_results,
                             predictions=cached_data.get('predictions_summary', {}))
    except Exception as e:
        return render_template('error.html', message=f"Predictive analytics error: {e}")

@app.route('/prescriptive')
def prescriptive():
    """Prescriptive Analytics Dashboard"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        presc_analytics = PrescriptiveAnalytics(cached_data)
        analysis_results = presc_analytics.run_analysis()
        
        return render_template('prescriptive.html', 
                             results=analysis_results,
                             recommendations=cached_data.get('prescriptive_recommendations', {}))
    except Exception as e:
        return render_template('error.html', message=f"Prescriptive analytics error: {e}")

# API Endpoints for AJAX requests
@app.route('/api/descriptive')
def api_descriptive():
    """API endpoint for descriptive analytics data"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        desc_analytics = DescriptiveAnalytics(cached_data)
        results = desc_analytics.get_api_data()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diagnostic')
def api_diagnostic():
    """API endpoint for diagnostic analytics data"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        diag_analytics = DiagnosticAnalytics(cached_data)
        results = diag_analytics.get_api_data()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictive')
def api_predictive():
    """API endpoint for predictive analytics data"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        pred_analytics = PredictiveAnalytics(cached_data)
        results = pred_analytics.get_api_data()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prescriptive')
def api_prescriptive():
    """API endpoint for prescriptive analytics data"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        presc_analytics = PrescriptiveAnalytics(cached_data)
        results = presc_analytics.get_api_data()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh')
def api_refresh():
    """Refresh cached data"""
    global cached_data
    cached_data = load_data()
    return jsonify({'status': 'success', 'message': 'Data refreshed successfully'})

@app.route('/api/customer/<int:customer_id>')
def api_customer_detail(customer_id):
    """Get detailed information about a specific customer"""
    global cached_data
    
    if not cached_data:
        cached_data = load_data()
    
    try:
        # Get customer basic info
        customer = cached_data['customers'][cached_data['customers']['customer_id'] == customer_id]
        if customer.empty:
            return jsonify({'error': 'Customer not found'}), 404
        
        # Get customer transactions
        transactions = cached_data['transactions'][cached_data['transactions']['customer_id'] == customer_id]
        
        # Get customer predictions if available
        predictions = {}
        if not cached_data['customer_predictions'].empty:
            pred_data = cached_data['customer_predictions'][cached_data['customer_predictions']['customer_id'] == customer_id]
            if not pred_data.empty:
                predictions = pred_data.iloc[0].to_dict()
        
        result = {
            'customer_info': customer.iloc[0].to_dict(),
            'transaction_summary': {
                'total_transactions': len(transactions),
                'total_spent': float(transactions['total_amount'].sum()),
                'avg_order_value': float(transactions['total_amount'].mean()) if len(transactions) > 0 else 0,
                'first_purchase': transactions['transaction_date'].min() if len(transactions) > 0 else None,
                'last_purchase': transactions['transaction_date'].max() if len(transactions) > 0 else None
            },
            'predictions': predictions
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/methodology')
def methodology():
    """Analytics Methodology Explanation Page"""
    return render_template('methodology.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message="Internal server error"), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('analytics', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
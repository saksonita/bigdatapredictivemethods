"""
Prescriptive Analytics Module
Handles "What Should We Do?" analysis for the web application
"""

import pandas as pd
import numpy as np
from datetime import datetime

class PrescriptiveAnalytics:
    def __init__(self, data):
        self.customers = data['customers']
        self.products = data['products']
        self.transactions = data['transactions']
        self.customer_predictions = data.get('customer_predictions', pd.DataFrame())
        
        # Convert date columns
        self.transactions['transaction_date'] = pd.to_datetime(self.transactions['transaction_date'])
        
        # Ensure required columns exist with proper names
        if 'unit_price' in self.transactions.columns and 'total_amount' not in self.transactions.columns:
            self.transactions['total_amount'] = self.transactions['unit_price'] * self.transactions['quantity'] * (1 - self.transactions.get('discount', 0))
        
        # Merge customer data with predictions if available
        if not self.customer_predictions.empty:
            self.customers_with_predictions = self.customers.merge(
                self.customer_predictions, on='customer_id', how='left'
            )
        else:
            self.customers_with_predictions = self.customers.copy()
            self.customers_with_predictions['churn_probability'] = 0.3  # Default assumption
            self.customers_with_predictions['predicted_clv'] = 200  # Default CLV
    
    def run_analysis(self):
        """Run complete prescriptive analysis"""
        results = {
            'retention_optimization': self._optimize_retention(),
            'marketing_optimization': self._optimize_marketing(),
            'pricing_optimization': self._optimize_pricing(),
            'inventory_optimization': self._optimize_inventory(),
            'resource_allocation': self._optimize_resources(),
            'action_plan': self._create_action_plan(),
            'roi_analysis': self._analyze_roi(),
            'charts': self._generate_charts()
        }
        return results
    
    def _optimize_retention(self):
        """Generate customer retention optimization strategies"""
        # Identify high-risk customers
        if 'churn_probability' in self.customers_with_predictions.columns:
            high_risk_customers = self.customers_with_predictions[
                self.customers_with_predictions['churn_probability'] > 0.7
            ].copy()
        else:
            # Fallback: use support tickets and transaction recency
            customer_summary = self.transactions.groupby('customer_id').agg({
                'transaction_date': 'max',
                'total_amount': 'sum'
            })
            current_date = self.transactions['transaction_date'].max()
            customer_summary['days_since_last'] = (current_date - customer_summary['transaction_date']).dt.days
            
            high_risk_customers = self.customers.merge(customer_summary, on='customer_id', how='left')
            high_risk_customers = high_risk_customers[high_risk_customers['days_since_last'] > 90]
            high_risk_customers['churn_probability'] = 0.8  # Assign high probability
        
        # Retention campaign scenarios
        retention_scenarios = []
        campaign_costs = [50, 100, 200, 500]
        retention_lifts = [0.1, 0.2, 0.35, 0.5]
        
        if len(high_risk_customers) > 0:
            avg_clv = high_risk_customers.get('predicted_clv', high_risk_customers.get('total_amount', pd.Series([200]))).mean()
            if pd.isna(avg_clv) or avg_clv == 0:
                avg_clv = 200
            
            for cost, lift in zip(campaign_costs, retention_lifts):
                customers_saved = len(high_risk_customers) * lift
                revenue_saved = customers_saved * avg_clv
                total_cost = len(high_risk_customers) * cost
                roi = (revenue_saved - total_cost) / total_cost * 100 if total_cost > 0 else 0
                
                retention_scenarios.append({
                    'campaign_cost_per_customer': cost,
                    'retention_lift': f"{lift:.0%}",
                    'customers_saved': int(customers_saved),
                    'revenue_saved': float(revenue_saved),
                    'total_campaign_cost': float(total_cost),
                    'roi_percentage': float(roi)
                })
        
        # Recommended strategy
        if retention_scenarios:
            best_scenario = max(retention_scenarios, key=lambda x: x['roi_percentage'])
        else:
            best_scenario = {}
        
        return {
            'high_risk_customers': {
                'count': len(high_risk_customers),
                'avg_churn_probability': float(high_risk_customers.get('churn_probability', pd.Series([0])).mean()),
                'total_value_at_risk': float(high_risk_customers.get('predicted_clv', high_risk_customers.get('total_amount', pd.Series([0]))).sum())
            },
            'retention_scenarios': retention_scenarios,
            'recommended_strategy': best_scenario,
            'tactical_recommendations': [
                "Implement personal account manager for high-risk customers",
                "Launch VIP discount program (15-25% off)",
                "Provide priority customer support",
                "Offer early access to new products",
                "Accelerate loyalty rewards program"
            ]
        }
    
    def _optimize_marketing(self):
        """Generate marketing campaign optimization strategies"""
        # Customer segmentation for marketing
        active_customers = self.customers_with_predictions[
            self.customers_with_predictions.get('churn_probability', 0.3) < 0.7
        ].copy()
        
        if len(active_customers) == 0:
            return {'message': 'No active customers for marketing optimization'}
        
        # Create marketing segments
        active_customers['marketing_segment'] = 'Standard'
        
        if 'predicted_clv' in active_customers.columns:
            clv_75th = active_customers['predicted_clv'].quantile(0.75)
            active_customers.loc[active_customers['predicted_clv'] > clv_75th, 'marketing_segment'] = 'High Value'
        
        if 'churn_probability' in active_customers.columns:
            active_customers.loc[active_customers['churn_probability'] > 0.4, 'marketing_segment'] = 'At Risk'
            active_customers.loc[
                (active_customers['predicted_clv'] > active_customers['predicted_clv'].quantile(0.75)) & 
                (active_customers['churn_probability'] > 0.4), 'marketing_segment'
            ] = 'High Value At Risk'
        
        # Campaign budget optimization
        total_marketing_budget = 100000
        campaigns = []
        
        for segment in active_customers['marketing_segment'].unique():
            segment_customers = active_customers[active_customers['marketing_segment'] == segment]
            
            # Define campaign parameters by segment
            if segment == 'High Value':
                cost_per_customer = 100
                conversion_rate = 0.15
                avg_order_lift = 1.3
            elif segment == 'High Value At Risk':
                cost_per_customer = 150
                conversion_rate = 0.12
                avg_order_lift = 1.4
            elif segment == 'At Risk':
                cost_per_customer = 75
                conversion_rate = 0.08
                avg_order_lift = 1.2
            else:  # Standard
                cost_per_customer = 25
                conversion_rate = 0.05
                avg_order_lift = 1.1
            
            max_customers = int(total_marketing_budget * 0.25 / cost_per_customer)
            target_customers = min(len(segment_customers), max_customers)
            
            campaign_cost = target_customers * cost_per_customer
            expected_conversions = target_customers * conversion_rate
            avg_clv = segment_customers.get('predicted_clv', pd.Series([200])).mean()
            if pd.isna(avg_clv):
                avg_clv = 200
            
            expected_revenue = expected_conversions * avg_clv * avg_order_lift
            roi = (expected_revenue - campaign_cost) / campaign_cost * 100 if campaign_cost > 0 else 0
            
            campaigns.append({
                'segment': segment,
                'target_customers': target_customers,
                'cost_per_customer': cost_per_customer,
                'campaign_cost': float(campaign_cost),
                'expected_conversions': int(expected_conversions),
                'expected_revenue': float(expected_revenue),
                'roi_percentage': float(roi)
            })
        
        # Sort by ROI
        campaigns = sorted(campaigns, key=lambda x: x['roi_percentage'], reverse=True)
        
        return {
            'segment_analysis': {
                seg: len(active_customers[active_customers['marketing_segment'] == seg])
                for seg in active_customers['marketing_segment'].unique()
            },
            'campaign_optimization': campaigns,
            'budget_allocation': {
                'total_budget': total_marketing_budget,
                'allocated_budget': sum(c['campaign_cost'] for c in campaigns),
                'expected_total_roi': sum(c['expected_revenue'] for c in campaigns) - sum(c['campaign_cost'] for c in campaigns)
            },
            'channel_recommendations': {
                'email': 'Best for retention and re-engagement',
                'social_media': 'Ideal for brand awareness and standard customers',
                'direct_mail': 'High-value customer appreciation',
                'sms': 'Urgent promotions and time-sensitive offers',
                'phone': 'High-value at-risk customer outreach'
            }
        }
    
    def _optimize_pricing(self):
        """Generate pricing optimization strategies"""
        # Analyze product performance
        product_performance = self.transactions.groupby('product_id').agg({
            'quantity': ['sum', 'mean'],
            'total_amount': 'sum',
            'transaction_id': 'count',
            'discount': 'mean'
        }).round(2)
        
        product_performance.columns = ['total_qty_sold', 'avg_qty_per_order', 
                                     'total_revenue', 'num_orders', 'avg_discount']
        
        # Merge with product data
        product_analysis = self.products.merge(product_performance, on='product_id', how='left')
        product_analysis = product_analysis.fillna(0)
        
        # Calculate profit margins (assuming 60% cost ratio)
        product_analysis['profit_margin'] = product_analysis['price'] * 0.4
        
        # Categorize products
        products_with_sales = product_analysis[product_analysis['total_qty_sold'] > 0].copy()
        
        if len(products_with_sales) > 0:
            # Define product categories based on performance
            high_volume_threshold = products_with_sales['total_qty_sold'].quantile(0.8)
            high_margin_threshold = products_with_sales['profit_margin'].quantile(0.8)
            
            def categorize_product(row):
                if row['total_qty_sold'] >= high_volume_threshold and row['profit_margin'] >= high_margin_threshold:
                    return 'Star Products'
                elif row['total_qty_sold'] >= high_volume_threshold:
                    return 'Cash Cows'
                elif row['profit_margin'] >= high_margin_threshold:
                    return 'High Margin'
                elif row['total_qty_sold'] < products_with_sales['total_qty_sold'].quantile(0.2):
                    return 'Low Performers'
                else:
                    return 'Standard'
            
            products_with_sales['product_category'] = products_with_sales.apply(categorize_product, axis=1)
            
            category_summary = products_with_sales.groupby('product_category').agg({
                'product_id': 'count',
                'total_revenue': 'sum',
                'profit_margin': 'mean'
            }).round(2)
        else:
            category_summary = pd.DataFrame()
        
        # Pricing recommendations
        pricing_strategies = {
            'Star Products': {
                'strategy': 'Premium Pricing',
                'price_change': '+5-10%',
                'rationale': 'High demand and margin - can support price increases'
            },
            'Cash Cows': {
                'strategy': 'Competitive Pricing',
                'price_change': '0-5%',
                'rationale': 'High volume products - maintain competitive pricing'
            },
            'High Margin': {
                'strategy': 'Value-Based Pricing',
                'price_change': '+3-7%',
                'rationale': 'Focus on value proposition and reduce discounts'
            },
            'Low Performers': {
                'strategy': 'Clearance Pricing',
                'price_change': '-20-40%',
                'rationale': 'Clear inventory and consider discontinuation'
            }
        }
        
        return {
            'product_categorization': {
                str(cat): {
                    'product_count': int(data['product_id']),
                    'total_revenue': float(data['total_revenue']),
                    'avg_margin': float(data['profit_margin'])
                } for cat, data in category_summary.iterrows()
            } if not category_summary.empty else {},
            'pricing_strategies': pricing_strategies,
            'optimization_opportunities': [
                "Increase prices by 5-10% for star products",
                "Implement dynamic pricing for high-demand items",
                "Reduce discount frequency on high-margin products",
                "Bundle slow-moving items with popular products"
            ]
        }
    
    def _optimize_inventory(self):
        """Generate inventory optimization recommendations"""
        # Analyze product demand patterns
        product_demand = self.transactions.groupby('product_id').agg({
            'quantity': ['sum', 'std'],
            'total_amount': 'sum'
        }).round(2)
        
        product_demand.columns = ['total_demand', 'demand_variability', 'total_revenue']
        
        # Merge with product info
        inventory_analysis = self.products.merge(product_demand, on='product_id', how='left')
        inventory_analysis = inventory_analysis.fillna(0)
        
        # Calculate demand categories
        if len(inventory_analysis[inventory_analysis['total_demand'] > 0]) > 0:
            high_demand_threshold = inventory_analysis['total_demand'].quantile(0.8)
            
            def get_inventory_recommendation(row):
                if row['total_demand'] >= high_demand_threshold:
                    return {
                        'action': 'Increase inventory by 25-40%',
                        'priority': 'High',
                        'reason': 'High demand product - ensure stock availability'
                    }
                elif row['total_demand'] < inventory_analysis['total_demand'].quantile(0.2):
                    return {
                        'action': 'Reduce inventory by 30-50%',
                        'priority': 'Medium',
                        'reason': 'Low demand - optimize storage costs'
                    }
                else:
                    return {
                        'action': 'Maintain current levels',
                        'priority': 'Low',
                        'reason': 'Stable demand pattern'
                    }
            
            # Apply recommendations
            inventory_analysis['recommendation'] = inventory_analysis.apply(get_inventory_recommendation, axis=1)
        
        # Category-level analysis
        category_demand = self.transactions.merge(self.products, on='product_id').groupby('category').agg({
            'quantity': ['sum', 'std'],
            'total_amount': 'sum'
        }).round(2)
        
        category_demand.columns = ['total_quantity', 'demand_variability', 'total_revenue']
        category_demand = category_demand.sort_values('total_quantity', ascending=False)
        
        return {
            'category_demand': {
                cat: {
                    'total_quantity': int(data['total_quantity']),
                    'demand_variability': float(data['demand_variability']),
                    'total_revenue': float(data['total_revenue'])
                } for cat, data in category_demand.iterrows()
            },
            'inventory_strategies': [
                "Increase safety stock for top 20% of products",
                "Implement just-in-time for low-demand items",
                "Use ABC analysis for inventory prioritization",
                "Monitor demand patterns weekly for adjustment"
            ],
            'optimization_opportunities': [
                "Reduce stockouts by 20% through better forecasting",
                "Decrease inventory holding costs by 15%",
                "Improve product availability to 99% for star products"
            ]
        }
    
    def _optimize_resources(self):
        """Generate resource allocation optimization"""
        # Define investment opportunities
        investment_opportunities = [
            {
                'initiative': 'Customer Retention Program',
                'required_investment': 150000,
                'expected_roi': 2.5,
                'implementation_time_months': 3,
                'risk_level': 'Low'
            },
            {
                'initiative': 'Marketing Campaign Optimization',
                'required_investment': 100000,
                'expected_roi': 3.2,
                'implementation_time_months': 2,
                'risk_level': 'Medium'
            },
            {
                'initiative': 'Pricing Optimization Engine',
                'required_investment': 120000,
                'expected_roi': 2.8,
                'implementation_time_months': 4,
                'risk_level': 'High'
            },
            {
                'initiative': 'Inventory Management System',
                'required_investment': 200000,
                'expected_roi': 1.8,
                'implementation_time_months': 6,
                'risk_level': 'Medium'
            },
            {
                'initiative': 'Product Recommendation System',
                'required_investment': 80000,
                'expected_roi': 4.0,
                'implementation_time_months': 3,
                'risk_level': 'Low'
            }
        ]
        
        # Calculate efficiency scores
        for opp in investment_opportunities:
            opp['efficiency_score'] = opp['expected_roi'] / opp['implementation_time_months']
            opp['expected_return'] = opp['required_investment'] * opp['expected_roi']
            opp['net_profit'] = opp['expected_return'] - opp['required_investment']
        
        # Sort by efficiency score
        sorted_opportunities = sorted(investment_opportunities, key=lambda x: x['efficiency_score'], reverse=True)
        
        # Budget allocation (assuming $500K budget)
        total_budget = 500000
        allocated_initiatives = []
        remaining_budget = total_budget
        
        for opp in sorted_opportunities:
            if opp['required_investment'] <= remaining_budget:
                allocated_initiatives.append(opp)
                remaining_budget -= opp['required_investment']
        
        total_investment = sum(init['required_investment'] for init in allocated_initiatives)
        total_return = sum(init['expected_return'] for init in allocated_initiatives)
        portfolio_roi = total_return / total_investment if total_investment > 0 else 0
        
        return {
            'investment_opportunities': sorted_opportunities,
            'recommended_allocation': allocated_initiatives,
            'budget_summary': {
                'total_budget': total_budget,
                'allocated_budget': total_investment,
                'remaining_budget': remaining_budget,
                'expected_return': total_return,
                'portfolio_roi': float(portfolio_roi)
            },
            'resource_priorities': [
                "Allocate 40% of resources to customer retention",
                "Invest 35% in marketing optimization",
                "Dedicate 25% to analytics and infrastructure",
                "Hire additional data analyst for model maintenance"
            ]
        }
    
    def _create_action_plan(self):
        """Create comprehensive action plan with priorities"""
        actions = [
            {
                'action': 'Deploy High-Risk Customer Retention Program',
                'priority': 'High',
                'timeline': '2-4 weeks',
                'budget': 150000,
                'expected_impact': 'Reduce churn by 15%',
                'success_metrics': ['Churn rate reduction', 'Customer satisfaction scores']
            },
            {
                'action': 'Implement Premium Pricing Strategy',
                'priority': 'High',
                'timeline': '1-2 weeks',
                'budget': 25000,
                'expected_impact': 'Increase revenue by 8-12%',
                'success_metrics': ['Revenue per product', 'Profit margins']
            },
            {
                'action': 'Launch Targeted Marketing Campaigns',
                'priority': 'Medium',
                'timeline': '3-4 weeks',
                'budget': 100000,
                'expected_impact': 'Improve campaign ROI by 40%',
                'success_metrics': ['Campaign conversion rates', 'Customer acquisition cost']
            },
            {
                'action': 'Optimize Inventory Levels',
                'priority': 'Medium',
                'timeline': '1-2 weeks',
                'budget': 50000,
                'expected_impact': 'Reduce stockouts by 20%',
                'success_metrics': ['Stock availability', 'Inventory turnover']
            }
        ]
        
        return {
            'immediate_actions': [a for a in actions if a['priority'] == 'High'],
            'medium_term_actions': [a for a in actions if a['priority'] == 'Medium'],
            'success_kpis': [
                'Customer churn rate reduction of 15%',
                'Revenue per customer increase of 25%',
                'Marketing ROI improvement of 40%',
                'Inventory optimization savings of 15%'
            ]
        }
    
    def _analyze_roi(self):
        """Analyze return on investment for recommendations"""
        # Calculate total investment and returns
        retention_investment = 150000
        retention_return = retention_investment * 2.5
        
        marketing_investment = 100000
        marketing_return = marketing_investment * 3.2
        
        pricing_investment = 25000
        pricing_return = pricing_investment * 1.8
        
        inventory_investment = 50000
        inventory_return = inventory_investment * 1.4
        
        total_investment = retention_investment + marketing_investment + pricing_investment + inventory_investment
        total_return = retention_return + marketing_return + pricing_return + inventory_return
        overall_roi = (total_return - total_investment) / total_investment
        
        return {
            'investment_breakdown': {
                'retention': {'investment': retention_investment, 'return': retention_return},
                'marketing': {'investment': marketing_investment, 'return': marketing_return},
                'pricing': {'investment': pricing_investment, 'return': pricing_return},
                'inventory': {'investment': inventory_investment, 'return': inventory_return}
            },
            'total_summary': {
                'total_investment': total_investment,
                'total_return': total_return,
                'net_profit': total_return - total_investment,
                'overall_roi': float(overall_roi),
                'payback_period_months': 12 / (overall_roi + 1) if overall_roi > 0 else 12
            }
        }
    
    def _generate_charts(self):
        """Generate chart data for prescriptive visualization"""
        charts = {}
        
        # ROI comparison chart
        roi_analysis = self._analyze_roi()
        initiatives = list(roi_analysis['investment_breakdown'].keys())
        roi_values = [(roi_analysis['investment_breakdown'][init]['return'] - 
                      roi_analysis['investment_breakdown'][init]['investment']) / 
                     roi_analysis['investment_breakdown'][init]['investment'] 
                     for init in initiatives]
        
        charts['roi_comparison'] = {
            'x': initiatives,
            'y': roi_values,
            'type': 'bar',
            'title': 'ROI by Initiative'
        }
        
        return charts
    
    def get_api_data(self):
        """Get data formatted for API responses"""
        return self.run_analysis()
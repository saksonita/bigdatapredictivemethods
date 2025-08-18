# Big Data Predictive Methods

This is a repository for my class containing data analytics and predictive modeling projects.

## W1 - Week 1: Dataset Generation and Descriptive Analytics

### 📊 generate_dataset.py
A comprehensive e-commerce dataset generator that creates realistic business data for analytics practice.

**What it does:**
- Generates 5 interconnected datasets: customers, products, transactions, marketing campaigns, and support tickets
- Creates 5,000 customers with realistic demographics and behavior patterns
- Produces 1,000 products across 8 categories with pricing and supplier information
- Simulates 50,000 transactions with seasonal patterns and customer preferences
- Includes marketing campaigns and customer support data
- Adds customer lifecycle metrics including churn indicators
- Exports all data to CSV files in the `dataset/` directory

**Key Features:**
- Reproducible data generation (uses fixed random seeds)
- Realistic business patterns (seasonal sales, customer segments, Pareto distribution)
- Connected data relationships across all tables
- Customer churn simulation for predictive modeling practice

### 📈 descriptive.ipynb
A comprehensive descriptive analytics notebook that analyzes the generated e-commerce data.

**What it does:**
- **Sales Performance Analysis**: Monthly/yearly revenue trends, growth rates, and order patterns
- **Customer Behavior Analysis**: Segment analysis, age demographics, top customers, and spending patterns
- **Product Performance Analysis**: Best-selling products, category performance, and revenue distribution
- **Seasonal Trends Analysis**: Monthly seasonality patterns and day-of-week analysis
- **Customer Lifecycle Analysis**: Acquisition trends, churn analysis, and purchase recency
- **Revenue Concentration Analysis**: Pareto principle validation (80/20 rule)
- **Business Metrics Summary**: Key performance indicators and recent performance metrics

**Key Insights Generated:**
- Overall revenue performance: $2.27M across 50K transactions
- Customer churn rate: 29.7% with retention opportunities identified
- Seasonal patterns in sales and customer behavior
- Product category performance rankings
- Customer segment behavioral differences

**Output:**
- Comprehensive data analysis with visualizations
- Business metrics summary
- Actionable insights for further diagnostic analysis
- Saves summary metrics to `descriptive_summary.json` for downstream analysis

Both scripts work together to create a complete data analytics workflow from data generation through descriptive analysis.

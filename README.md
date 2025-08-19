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

### 🌐 Flask Analytics Web Application
A comprehensive Flask web application that implements all four types of analytics in an interactive dashboard.

**What it includes:**
- **Interactive Dashboards**: Web-based interface for all analytics types
- **Real-time Analysis**: Dynamic data processing and visualization
- **Educational Content**: Built-in methodology explanations
- **API Endpoints**: RESTful APIs for programmatic access
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5

**Access the Application:**
```bash
cd W1
python run.py
# Open http://localhost:5000 in your browser
```

Both scripts and the web application work together to create a complete data analytics workflow from data generation through all four types of business analytics.

---

# 📚 Analytics Methodology - How We Got These Results

Understanding the methods and techniques behind each type of analytics helps you interpret results and apply similar approaches to other business problems.

## 1. 📊 Descriptive Analytics - "What Happened?"

### Statistical Aggregation Methods
- **Group-by Operations**: Used `groupby()` to segment customers by demographics and behavior
- **Value Counting**: Applied `value_counts()` for distribution analysis (cities, segments)
- **Statistical Summaries**: Used `describe()` for mean, standard deviation, quartiles

### Temporal Analysis Techniques
- **Time Series Grouping**: `dt.to_period('M')` for monthly trends
- **Day-of-Week Patterns**: `dt.day_name()` to identify weekly cycles
- **Hourly Analysis**: `dt.hour` for daily activity patterns

### Customer Segmentation - RFM Analysis

**Recency (R)**: Days since last purchase
```python
(current_date - last_purchase).days
```

**Frequency (F)**: Number of transactions
```python
transaction_count
```

**Monetary (M)**: Total spending amount
```python
total_amount.sum()
```

### Quantile-Based Segmentation
Used `pd.qcut()` to create value tiers (Bronze, Silver, Gold, Platinum) based on spending distribution.

---

## 2. 🔍 Diagnostic Analytics - "Why Did It Happen?"

### Statistical Testing Methods

#### Chi-Square Test
- **Purpose**: Test relationship between categorical variables and churn
- **Formula**: χ² = Σ[(Observed - Expected)² / Expected]
- **Usage**: Customer segment vs churn rate
- **Code**: `chi2_contingency(contingency_table)`

#### T-Test
- **Purpose**: Compare means between two groups
- **Formula**: t = (mean₁ - mean₂) / SE
- **Usage**: Spending: Churned vs Retained customers
- **Code**: `stats.ttest_ind(group1, group2)`

### Correlation Analysis
**Pearson Correlation**: Measures linear relationship between variables (-1 to +1)
- **r > 0.7**: Strong positive correlation
- **0.3 < r < 0.7**: Moderate correlation
- **r < 0.3**: Weak correlation

```python
dataframe.corr()
```

### Behavioral Analysis Techniques
- **Cohort Analysis**: Track customer behavior over time by segments
- **Price Elasticity**: `correlation(price, quantity)`
- **Pareto Analysis**: Identify top 20% customers generating 80% revenue

---

## 3. 🔮 Predictive Analytics - "What Will Happen?"

### Machine Learning Models

#### Random Forest Classifier
- **Purpose**: Predict customer churn probability
- **How it works**: Combines multiple decision trees
- **Input Features**: Age, spending, frequency, support tickets
- **Output**: Probability (0-1) of churning
- **Code**: `RandomForestClassifier(n_estimators=100)`

#### Random Forest Regressor
- **Purpose**: Predict Customer Lifetime Value (CLV)
- **How it works**: Ensemble of regression trees
- **Target**: Future customer spending
- **Evaluation**: R² score, RMSE
- **Code**: `RandomForestRegressor(n_estimators=100)`

### Feature Engineering Process
1. **Aggregation Features**: Sum, mean, std of transactions per customer
2. **Temporal Features**: Days active, days since last purchase
3. **Behavioral Features**: Purchase frequency, discount sensitivity
4. **Support Features**: Ticket count, resolution time
5. **Encoding**: Convert categorical to numerical using LabelEncoder

### Time Series Forecasting
**Sales Forecast Formula**:
```python
forecast[t+1] = current_value × (1 + growth_rate)^t
```
- **Growth Rate**: (Recent 7-day avg - Previous 7-day avg) / Previous avg
- **Trend Analysis**: Linear regression on historical data

### Model Evaluation Metrics
- **Classification Accuracy**: (Correct Predictions) / (Total Predictions)
- **R² Score**: 1 - (SS_res / SS_tot) [Regression quality]
- **RMSE**: √(Σ(predicted - actual)² / n) [Prediction error]

---

## 4. 💡 Prescriptive Analytics - "What Should We Do?"

### Optimization Techniques

#### Customer Retention
- **Method**: Risk-based prioritization
- **Rule**: Churn probability > 70% → Immediate intervention
- **ROI Focus**: High-value customers first

#### Resource Allocation
- **Method**: CLV-based segmentation
- **Rule**: CLV > 75th percentile → VIP treatment
- **Efficiency**: Maximize ROI per dollar spent

#### Inventory Optimization
- **Method**: Demand forecasting
- **Rule**: Stock level = Predicted demand × Safety factor
- **Goal**: Minimize stockouts and overstock

### Decision Framework

| Customer Risk Level | Customer Value | Recommended Action | Method |
|-------------------|----------------|-------------------|---------|
| High Risk (>70%) | High Value (Top 25%) | Personal call + Special offer | Manual intervention |
| High Risk (>70%) | Medium Value | Email campaign + Discount | Automated campaign |
| Medium Risk (30-70%) | High Value | Loyalty program invitation | Engagement strategy |
| Low Risk (<30%) | High Value | Upselling opportunities | Growth strategy |

### ROI Calculation
**Formula**: ROI = (Benefit - Cost) / Cost × 100%
- **Retention Benefit**: Customer CLV × Retention probability improvement
- **Campaign Cost**: Per-customer campaign cost
- **Break-even**: Cost < (CLV × Probability improvement)

---

## 🔑 Key Statistical & ML Concepts Used

### Statistical Methods
- **Descriptive Statistics**: Mean, median, std, quartiles
- **Inferential Statistics**: Hypothesis testing
- **Correlation Analysis**: Pearson correlation
- **Distribution Analysis**: Histograms, quantiles

### Data Processing
- **Missing Values**: `fillna()` with business logic
- **Date Parsing**: `pd.to_datetime()`
- **Feature Engineering**: Create new meaningful variables
- **Encoding**: Convert categories to numbers

### Machine Learning
- **Supervised Learning**: Classification & regression
- **Ensemble Methods**: Random Forest algorithms
- **Model Validation**: Train-test split
- **Feature Importance**: Identify key predictors

### Business Intelligence
- **KPI Calculation**: Churn rate, CLV, AOV
- **Segmentation**: Value, behavior, risk-based
- **Cohort Analysis**: Track groups over time
- **Portfolio Optimization**: Risk-return balance

---

## 🎓 Teaching Points for Students

1. **Start with Questions**: Always begin with business questions before choosing methods
2. **Data Quality First**: Clean, validate, and understand your data
3. **Choose Appropriate Methods**: Match statistical/ML methods to your data and goals
4. **Validate Results**: Use proper evaluation metrics and cross-validation
5. **Interpret Business Impact**: Translate technical results into actionable insights
6. **Iterate and Improve**: Analytics is an ongoing process, not a one-time activity

---

## 📁 Project Structure

```
W1/
├── app.py                          # Flask web application
├── run.py                          # Application startup script
├── requirements.txt                # Python dependencies
├── analytics/                      # Analytics modules
│   ├── descriptive_analytics.py   # Descriptive analysis methods
│   ├── diagnostic_analytics.py    # Diagnostic analysis methods
│   ├── predictive_analytics.py    # Predictive analysis methods
│   └── prescriptive_analytics.py  # Prescriptive analysis methods
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Dashboard homepage
│   ├── descriptive.html           # Descriptive analytics page
│   ├── diagnostic.html            # Diagnostic analytics page
│   ├── predictive.html            # Predictive analytics page
│   ├── prescriptive.html          # Prescriptive analytics page
│   └── methodology.html           # Methodology explanation page
├── static/                        # Static assets
│   ├── css/style.css             # Custom styling
│   └── js/app.js                 # JavaScript functionality
└── dataset/                       # Generated datasets
    ├── customers.csv              # Customer data
    ├── products.csv               # Product catalog
    ├── transactions.csv           # Transaction records
    ├── support_tickets.csv        # Customer support data
    └── marketing_campaigns.csv    # Marketing campaign data
```

This comprehensive methodology serves as both a learning resource and a reference guide for understanding how modern business analytics translates data into actionable insights.

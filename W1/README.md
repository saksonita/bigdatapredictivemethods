# E-commerce Analytics Dashboard

A comprehensive Flask web application that provides end-to-end analytics for e-commerce businesses, featuring descriptive, diagnostic, predictive, and prescriptive analytics with interactive dashboards and machine learning models.

## 🚀 Features

### 📊 Descriptive Analytics - "What Happened?"
- Customer demographics and segmentation analysis
- Sales performance metrics and trends
- Product performance analysis
- Temporal patterns and seasonal trends
- Interactive charts and visualizations

### 🔍 Diagnostic Analytics - "Why Did It Happen?"
- Customer churn factor analysis
- Revenue driver identification
- Customer behavior pattern analysis
- Statistical correlation analysis
- Support impact assessment

### 🔮 Predictive Analytics - "What Will Happen?"
- Customer churn prediction using machine learning
- Customer Lifetime Value (CLV) forecasting
- Sales forecasting and trend prediction
- Product demand forecasting
- Risk analysis and customer segmentation

### 💡 Prescriptive Analytics - "What Should We Do?"
- Customer retention optimization strategies
- Marketing campaign optimization with ROI analysis
- Pricing and inventory optimization recommendations
- Resource allocation and budget optimization
- Actionable implementation roadmaps

## 🛠️ Technology Stack

- **Backend:** Flask (Python web framework)
- **Data Processing:** Pandas, NumPy, SciPy
- **Machine Learning:** Scikit-learn
- **Visualization:** Plotly.js, Chart.js
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment:** Gunicorn (production server)

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone or Download the Project
```bash
# If you have the files locally, navigate to the project directory
cd bigdatapredictivemethods/W1
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv analytics_env

# Activate virtual environment
# On Windows:
analytics_env\Scripts\activate
# On macOS/Linux:
source analytics_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Data Files
Ensure the following data files exist in the `dataset/` directory:
- `customers.csv`
- `products.csv`
- `transactions.csv`
- `support_tickets.csv`
- `marketing_campaigns.csv`

### 5. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📁 Project Structure

```
W1/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── analytics/                     # Analytics modules
│   ├── __init__.py
│   ├── descriptive_analytics.py   # Descriptive analytics logic
│   ├── diagnostic_analytics.py    # Diagnostic analytics logic
│   ├── predictive_analytics.py    # Predictive analytics logic
│   └── prescriptive_analytics.py  # Prescriptive analytics logic
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Dashboard homepage
│   ├── descriptive.html           # Descriptive analytics page
│   ├── prescriptive.html          # Prescriptive analytics page
│   └── error.html                 # Error page
├── static/                        # Static files
│   ├── css/
│   │   └── style.css              # Custom CSS styles
│   └── js/
│       └── app.js                 # JavaScript functionality
└── dataset/                       # Data files
    ├── customers.csv
    ├── products.csv
    ├── transactions.csv
    ├── support_tickets.csv
    └── marketing_campaigns.csv
```

## 🎯 Usage Guide

### Navigation
- **Dashboard:** Overview of key metrics and analytics types
- **Descriptive:** Historical data analysis and trends
- **Diagnostic:** Root cause analysis and correlations
- **Predictive:** Machine learning predictions and forecasts
- **Prescriptive:** Actionable recommendations and optimization strategies

### Key Features
1. **Interactive Dashboards:** Click through different analytics types
2. **Real-time Data:** Refresh data using the "Refresh Data" button
3. **Responsive Design:** Works on desktop, tablet, and mobile devices
4. **Export Capabilities:** Print reports and export data
5. **Customer Details:** Click on customer metrics for detailed information

## 🔧 Configuration

### Environment Variables
You can configure the application using environment variables:

```bash
# Optional: Set Flask environment
export FLASK_ENV=development  # or production

# Optional: Set debug mode
export FLASK_DEBUG=1  # or 0 for production

# Optional: Set custom port
export PORT=5000
```

### Production Deployment
For production deployment with Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## 📊 Data Requirements

The application expects CSV files with the following structure:

### customers.csv
- customer_id, first_name, last_name, email, age, gender, city, state, registration_date, customer_segment, is_churned

### products.csv
- product_id, product_name, category, price

### transactions.csv
- transaction_id, customer_id, product_id, transaction_date, quantity, total_amount, discount

### support_tickets.csv
- ticket_id, customer_id, priority, resolution_time_hours

### marketing_campaigns.csv
- campaign_id, campaign_name, start_date, end_date, budget, channel

## 🚀 API Endpoints

The application provides REST API endpoints for integration:

- `GET /api/descriptive` - Descriptive analytics data
- `GET /api/diagnostic` - Diagnostic analytics data
- `GET /api/predictive` - Predictive analytics data
- `GET /api/prescriptive` - Prescriptive analytics data
- `GET /api/customer/<id>` - Individual customer details
- `GET /api/refresh` - Refresh cached data

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Update color scheme in CSS variables at the top of the file

### Analytics Logic
- Extend analytics modules in the `analytics/` directory
- Add new visualizations in the HTML templates
- Customize machine learning models in the predictive analytics module

### Adding New Features
1. Create new analytics modules following the existing pattern
2. Add corresponding HTML templates
3. Update the main application routes
4. Add navigation links in the base template

## 📈 Performance Optimization

- **Caching:** The application caches analysis results
- **Auto-refresh:** Data refreshes automatically every 5 minutes
- **Lazy Loading:** Charts load on demand
- **Responsive Design:** Optimized for different screen sizes

## 🐛 Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Data File Not Found**
   - Ensure all CSV files are in the `dataset/` directory
   - Check file permissions

3. **Port Already in Use**
   ```bash
   # Use a different port
   python app.py --port 5001
   ```

4. **Memory Issues with Large Datasets**
   - Optimize data loading in analytics modules
   - Consider data sampling for very large datasets

### Debug Mode
Run the application in debug mode for detailed error messages:

```bash
export FLASK_DEBUG=1
python app.py
```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is provided as-is for educational and commercial use.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section
2. Review the code comments for implementation details
3. Ensure all dependencies are correctly installed

## 🎉 Acknowledgments

- Built with Flask and modern web technologies
- Uses Bootstrap for responsive design
- Implements machine learning with scikit-learn
- Visualizations powered by Plotly.js

---

**Ready to transform your e-commerce data into actionable insights!** 🚀
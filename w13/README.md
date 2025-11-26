# Qlik Dashboard Auto-Download Scraper

This script automatically scrapes data from the Qlik Sense dashboard at nongnet.or.kr.

## Features

- ✅ Automated browser control using Selenium
- ✅ Extracts table data from Qlik dashboards
- ✅ Exports data to JSON and Excel formats
- ✅ Takes screenshots of the dashboard
- ✅ Handles dynamic JavaScript content
- ✅ Configurable headless mode

## Requirements

- Python 3.8 or higher
- Chrome browser
- ChromeDriver (automatically managed by Selenium 4.15+)

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings (browser visible):
```bash
python auto_download.py
```

### Programmatic Usage

```python
from auto_download import QlikDashboardScraper

# Create scraper instance
scraper = QlikDashboardScraper(download_dir='./my_downloads')

# Run scraper
data = scraper.scrape(headless=False, take_screenshot_flag=True)

# Process the data
print(f"Extracted {len(data)} tables")
```

### Headless Mode

Run without opening a browser window:
```python
scraper = QlikDashboardScraper()
data = scraper.scrape(headless=True)
```

## Configuration

### Download Directory

By default, files are saved to `./downloads`. You can specify a custom directory:
```python
scraper = QlikDashboardScraper(download_dir='/path/to/downloads')
```

### Output Files

The scraper generates:
- `qlik_data_TIMESTAMP.json` - Raw data in JSON format
- `qlik_data_TIMESTAMP.xlsx` - Excel file with multiple sheets (if tabular data found)
- `dashboard_screenshot_TIMESTAMP.png` - Screenshot of the dashboard

## How It Works

1. **Browser Automation**: Launches Chrome with Selenium
2. **Page Loading**: Navigates to the Qlik dashboard URL with pre-selected filters
3. **Wait for Content**: Waits for dashboard objects to load
4. **Data Extraction**: Extracts data from tables and Qlik objects
5. **Export**: Saves data to JSON and Excel formats
6. **Screenshot**: Captures dashboard visualization
7. **Cleanup**: Closes browser and saves files

## NeuralProphet NumPy Compatibility Fix

### Problem
If you encounter this error when running NeuralProphet models:
```
AttributeError: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.
```

### Quick Fix
Run the automated fix script:
```bash
# Option 1: Python script (recommended)
python fix_numpy_compatibility.py

# Option 2: Bash script
bash fix_numpy_compatibility.sh

# Option 3: Manual fix
pip uninstall numpy -y
pip install "numpy<2.0,>=1.24.0"
```

### Detailed Instructions
See [NUMPY_FIX.md](NUMPY_FIX.md) for comprehensive troubleshooting and fix instructions.

## Troubleshooting

### ChromeDriver Issues

If you get ChromeDriver errors, ensure:
- Chrome browser is installed
- Selenium 4.15+ is installed (includes automatic driver management)

### No Data Extracted

If no data is extracted:
- Check the screenshot to see what's on the page
- The dashboard might require authentication
- Adjust wait times in the code if page loads slowly
- Check browser console for JavaScript errors

### Authentication Required

If the site requires login:
1. Modify the `load_page()` method to handle login
2. Add credentials management
3. Or use browser cookies from an authenticated session

## Customization

### Adjust Wait Times

If the dashboard loads slowly, increase wait times:
```python
time.sleep(5)  # Change to higher value
```

### Custom Selectors

If data extraction fails, update CSS selectors in:
- `wait_for_dashboard_load()` - Dashboard object selectors
- `extract_table_data()` - Table selectors
- `click_download_button()` - Download button selectors

### Additional Data Sources

To extract charts or other visualizations, modify `_extract_data_alternative()` method.

## Notes

- The URL includes pre-selected filters for "배추" (cabbage) data
- Date range is pre-selected (dates 45973-45986 in serial format)
- Qlik dashboards are dynamic - data extraction depends on page structure
- Some dashboards may have anti-scraping measures

## License

MIT License - Feel free to modify and use as needed.

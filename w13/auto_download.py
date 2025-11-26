# -*- coding: utf-8 -*-
"""
Auto-download script for Qlik Sense dashboard data
Scrapes data from: https://www.nongnet.or.kr/qlik/sso/single/
"""

import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd


class QlikDashboardScraper:
    def __init__(self, download_dir=None):
        """
        Initialize the Qlik dashboard scraper

        Args:
            download_dir (str): Directory to save downloaded files. Defaults to ./downloads
        """
        self.url = (
            "https://www.nongnet.or.kr/qlik/sso/single/"
            "?appid=075d5cd6-c045-45fa-8640-07873c49c4bb"
            "&sheet=edf72f21-8148-4fd7-aa8d-e3e61c560a0b"
            "&theme=theme_at_24"
            "&opt=ctxmenu,currsel"
            "&select=$::%ED%92%88%EB%AA%A9%EB%AA%85_%EC%84%A0%ED%83%9D,%ED%86%A0%EB%A7%88%ED%86%A0"
            "&select=$::%EB%8C%80%EC%83%81%EC%9D%BC%EC%9E%90_%EC%84%A0%ED%83%9D,"
            "45973,45974,45975,45976,45977,45978,45979,45980,45981,45982,45983,45984,45985,45986"
        )

        if download_dir is None:
            download_dir = os.getcwd()

        self.download_dir = download_dir

        self.driver = None
        self.wait = None

    def setup_driver(self, headless=False):
        """
        Setup Chrome WebDriver with appropriate options

        Args:
            headless (bool): Run browser in headless mode
        """
        chrome_options = Options()

        if headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # Set download preferences
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

        print(f"✓ Chrome driver initialized")
        print(f"✓ Download directory: {self.download_dir}")

    def load_page(self):
        """Load the Qlik dashboard page"""
        print(f"\nLoading page...")
        self.driver.get(self.url)

        # Wait for page to load - adjust selector based on actual page structure
        time.sleep(5)  # Initial wait for Qlik to initialize

        print("✓ Page loaded")

    def wait_for_dashboard_load(self):
        """Wait for Qlik dashboard to fully load"""
        print("Waiting for dashboard to load...")

        try:
            # Wait for Qlik objects to be present
            # Common Qlik selectors - adjust based on actual dashboard
            possible_selectors = [
                "div.qv-object",
                "div.qv-panel-sheet",
                "article.qv-object",
                "[data-qv-object]",
                ".qv-gridcell"
            ]

            for selector in possible_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"✓ Found {len(elements)} dashboard objects using selector: {selector}")
                        time.sleep(3)  # Additional wait for data to populate
                        return True
                except:
                    continue

            print("⚠ Dashboard objects not found with common selectors, continuing anyway...")
            time.sleep(5)
            return True

        except TimeoutException:
            print("⚠ Timeout waiting for dashboard, continuing anyway...")
            return False

    def extract_table_data(self):
        """
        Extract table data from the dashboard

        Returns:
            list: List of dictionaries containing table data
        """
        print("\nExtracting table data...")

        tables_data = []

        # Try to find tables in the page
        table_selectors = [
            "table",
            "div[role='table']",
            ".qv-st-data-table table",
            "div.qv-object table"
        ]

        for selector in table_selectors:
            try:
                tables = self.driver.find_elements(By.CSS_SELECTOR, selector)

                if tables:
                    print(f"✓ Found {len(tables)} tables using selector: {selector}")

                    for idx, table in enumerate(tables):
                        try:
                            # Extract headers
                            headers = []
                            header_elements = table.find_elements(By.CSS_SELECTOR, "th")

                            if header_elements:
                                headers = [h.text.strip() for h in header_elements]
                            else:
                                # Try alternative header selectors
                                header_elements = table.find_elements(By.CSS_SELECTOR, "thead td")
                                headers = [h.text.strip() for h in header_elements]

                            # Extract rows
                            rows = []
                            row_elements = table.find_elements(By.CSS_SELECTOR, "tbody tr")

                            for row in row_elements:
                                cells = row.find_elements(By.CSS_SELECTOR, "td")
                                row_data = [cell.text.strip() for cell in cells]

                                if row_data:
                                    if headers and len(headers) == len(row_data):
                                        rows.append(dict(zip(headers, row_data)))
                                    else:
                                        rows.append(row_data)

                            if rows:
                                tables_data.append({
                                    'table_index': idx,
                                    'headers': headers,
                                    'data': rows
                                })
                                print(f"  ✓ Extracted table {idx}: {len(rows)} rows")

                        except Exception as e:
                            print(f"  ⚠ Error extracting table {idx}: {str(e)}")
                            continue

            except Exception:
                continue

        if not tables_data:
            print("⚠ No tables found, trying alternative extraction methods...")
            tables_data = self._extract_data_alternative()

        return tables_data

    def _extract_data_alternative(self):
        """Alternative data extraction method for non-table layouts"""
        print("Attempting alternative data extraction...")

        data = []

        # Try to extract text content from Qlik objects
        try:
            qlik_objects = self.driver.find_elements(By.CSS_SELECTOR, "div.qv-object")

            for idx, obj in enumerate(qlik_objects):
                try:
                    text_content = obj.text.strip()
                    if text_content:
                        data.append({
                            'object_index': idx,
                            'content': text_content
                        })
                        print(f"  ✓ Extracted content from object {idx}")
                except:
                    continue

        except Exception as e:
            print(f"⚠ Alternative extraction failed: {str(e)}")

        return data

    def click_download_button(self):
        """
        Attempt to find and click download/export button

        Returns:
            bool: True if download initiated, False otherwise
        """
        print("\nLooking for download button...")

        download_selectors = [
            "button[title*='Export']",
            "button[title*='Download']",
            "button[title*='데이터 저장']",  # "Data Save" in Korean
            "*[title*='데이터 저장']",
            "button[title*='다운로드']",  # "Download" in Korean
            "button[title*='내보내기']",  # "Export" in Korean
            "[aria-label*='export']",
            "[aria-label*='download']",
            "div.lui-icon--download",
            "button.export-data"
        ]

        for selector in download_selectors:
            try:
                buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)

                if buttons:
                    print(f"✓ Found download button with selector: {selector}")
                    buttons[0].click()
                    print("✓ Download button clicked")
                    time.sleep(3)
                    return True

            except Exception:
                continue

        print("⚠ No download button found")
        return False

    def save_data(self, data, filename=None):
        """
        Save extracted data to files

        Args:
            data (list): Data to save
            filename (str): Base filename (without extension)
        """
        if not data:
            print("⚠ No data to save")
            return

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qlik_data_{timestamp}"

        # Save as JSON
        json_path = os.path.join(self.download_dir, f"{filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Data saved to: {json_path}")

        # Try to save as Excel if data is tabular
        try:
            if isinstance(data, list) and data:
                # Check if data contains tables
                if isinstance(data[0], dict) and 'data' in data[0]:
                    excel_path = os.path.join(self.download_dir, f"{filename}.xlsx")

                    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                        for table in data:
                            if 'data' in table and table['data']:
                                df = pd.DataFrame(table['data'])
                                sheet_name = f"Table_{table.get('table_index', 0)}"
                                df.to_excel(writer, sheet_name=sheet_name, index=False)

                    print(f"✓ Data saved to: {excel_path}")

        except Exception as e:
            print(f"⚠ Could not save as Excel: {str(e)}")

    def take_screenshot(self, filename=None):
        """Take a screenshot of the dashboard"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dashboard_screenshot_{timestamp}.png"

        screenshot_path = os.path.join(self.download_dir, filename)
        self.driver.save_screenshot(screenshot_path)
        print(f"✓ Screenshot saved to: {screenshot_path}")

    def scrape(self, headless=False, take_screenshot_flag=True):
        """
        Main scraping method

        Args:
            headless (bool): Run browser in headless mode
            take_screenshot_flag (bool): Take screenshot of the dashboard

        Returns:
            list: Extracted data
        """
        try:
            self.setup_driver(headless=headless)
            self.load_page()
            self.wait_for_dashboard_load()

            # Take screenshot if requested
            if take_screenshot_flag:
                self.take_screenshot()

            # Try to find and click download button
            self.click_download_button()

            # Extract table data
            data = self.extract_table_data()

            # Save extracted data
            if data:
                self.save_data(data)

            return data

        except Exception as e:
            print(f"✗ Error during scraping: {str(e)}")
            raise

        finally:
            if self.driver:
                print("\nClosing browser...")
                time.sleep(2)
                self.driver.quit()
                print("✓ Browser closed")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


def main():
    """Main execution function"""
    print("=" * 60)
    print("Qlik Dashboard Data Scraper")
    print("=" * 60)

    # Create scraper instance
    scraper = QlikDashboardScraper()

    # Run scraper
    # Set headless=True to run without opening browser window
    data = scraper.scrape(headless=False, take_screenshot_flag=True)

    print("\n" + "=" * 60)
    print(f"Scraping completed!")
    print(f"Total items extracted: {len(data) if data else 0}")
    print("=" * 60)


if __name__ == "__main__":
    main()

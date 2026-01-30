"""
LinkDetective Scraper - Web Version (Render.com compatible)
"""

import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import os


st.set_page_config(
    page_title="LinkDetective Scraper",
    page_icon="🔗",
    layout="wide"
)

st.title("🔗 LinkDetective Scraper")
st.markdown("---")


def setup_driver():
    """Setup Chrome for cloud environment (Render.com)"""
    chrome_options = Options()
    
    # Headless mode
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-tools")
    
    # For Render.com (uses system chromium)
    chrome_options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)
    
    return driver


def scrape_linkdetective(url, progress_bar, status_text):
    """Main scraping function"""
    
    try:
        status_text.text("🚀 Starting browser...")
        driver = setup_driver()
        
        status_text.text("📂 Loading page...")
        driver.get(url)
        time.sleep(5)
        
        status_text.text("⏳ Waiting for data...")
        try:
            WebDriverWait(driver, 30).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, "table tbody tr")) > 0
            )
            time.sleep(3)
        except:
            status_text.text("❌ Data did not load")
            driver.quit()
            return None, "Error: Data did not load. Check URL."
        
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        
        if not rows or "No data available" in rows[0].text:
            driver.quit()
            return None, "Error: Table is empty"
        
        total_rows = len(rows)
        status_text.text(f"📊 Found {total_rows} domains. Starting collection...")
        
        all_data = []
        
        for idx, row in enumerate(rows, 1):
            try:
                progress_bar.progress(idx / total_rows)
                
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 2:
                    continue
                
                domain = None
                for cell in cells[1:4]:
                    txt = cell.text.strip()
                    if txt and '.' in txt and len(txt.split()) == 1:
                        domain = txt
                        break
                
                if not domain:
                    continue
                
                status_text.text(f"📍 [{idx}/{total_rows}] Processing: {domain}")
                
                try:
                    icon = row.find_element(By.CSS_SELECTOR, "td:last-child img, td:last-child [data-bs-toggle='modal']")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", icon)
                    time.sleep(2)
                    
                    modal = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal.show, div[role='dialog']"))
                    )
                    time.sleep(2)
                    
                    modal_table = modal.find_element(By.CSS_SELECTOR, "table tbody")
                    modal_rows = modal_table.find_elements(By.TAG_NAME, "tr")
                    
                    for mrow in modal_rows:
                        if "No data available" in mrow.text:
                            break
                        
                        mcells = mrow.find_elements(By.TAG_NAME, "td")
                        if len(mcells) >= 2:
                            seller = mcells[0].text.strip()
                            price = mcells[1].text.strip()
                            
                            if seller and seller != "No data available":
                                all_data.append({
                                    'domain': domain,
                                    'seller': seller,
                                    'price': price
                                })
                    
                    try:
                        close_btn = modal.find_element(By.CSS_SELECTOR, "button.close, button[data-bs-dismiss='modal']")
                        driver.execute_script("arguments[0].click();", close_btn)
                    except:
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                    
                    time.sleep(1)
                    
                except:
                    all_data.append({
                        'domain': domain,
                        'seller': '',
                        'price': ''
                    })
                
            except:
                continue
        
        driver.quit()
        
        if all_data:
            df = pd.DataFrame(all_data)
            return df, None
        else:
            return None, "Error: No data collected"
            
    except Exception as e:
        return None, f"Error: {str(e)}"


# Main UI
col1, col2 = st.columns([2, 1])

with col1:
    url = st.text_input(
        "🔗 Enter LinkDetective URL:",
        placeholder="https://linkdetective.pro?hash=YOUR_HASH",
        help="Paste the full URL from linkdetective.pro"
    )

with col2:
    st.write("")
    st.write("")
    start_button = st.button("🚀 Start Scraping", type="primary", use_container_width=True)

st.markdown("---")

if start_button:
    if not url or not url.startswith('http'):
        st.error("❌ Please enter a valid URL")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("Processing..."):
            df, error = scrape_linkdetective(url, progress_bar, status_text)
        
        progress_bar.empty()
        
        if error:
            st.error(f"❌ {error}")
            status_text.empty()
        else:
            status_text.empty()
            st.success("✅ Scraping completed successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Records", len(df))
            with col2:
                st.metric("🌐 Unique Domains", df['domain'].nunique())
            with col3:
                avg_sellers = df.groupby('domain').size().mean()
                st.metric("📈 Avg Sellers/Domain", f"{avg_sellers:.1f}")
            
            st.markdown("---")
            
            st.subheader("📋 Preview (first 20 rows)")
            st.dataframe(df.head(20), use_container_width=True)
            
            st.subheader("🏆 Top 10 Domains by Sellers")
            top_domains = df.groupby('domain').size().sort_values(ascending=False).head(10)
            st.bar_chart(top_domains)
            
            st.markdown("---")
            st.subheader("💾 Download Results")
            
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"linkdetective_results_{timestamp}.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **LinkDetective Scraper** extracts domain and seller information from linkdetective.pro.
    
    ### How to use:
    1. Paste your LinkDetective URL
    2. Click "Start Scraping"
    3. Wait for completion
    4. Download CSV file
    
    ### Features:
    - ✅ Cloud-based processing
    - ✅ Real-time progress
    - ✅ Data visualization
    - ✅ CSV export
    
    ### Hosted on:
    Render.com
    """)
    
    st.markdown("---")
    st.caption("v1.0 | Cloud Edition")

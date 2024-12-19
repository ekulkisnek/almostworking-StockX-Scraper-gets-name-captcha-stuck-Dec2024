import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def test_stockx_selenium():
    print("\nInitializing Chrome driver...")
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    # Set window size for headless mode
    options.add_argument('--window-size=1920,1080')
    # Disable various Chrome features to reduce memory usage
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images to speed up loading
    
    try:
        options.binary_location = "/nix/store/zi4f80l169xlmivz8vja8wlphq74qqk0-chromium-125.0.6422.141/bin/chromium"
        driver = uc.Chrome(options=options, browser_executable_path="/nix/store/zi4f80l169xlmivz8vja8wlphq74qqk0-chromium-125.0.6422.141/bin/chromium")
        url = 'https://stockx.com/air-jordan-1-retro-low-og-sp-travis-scott-olive-w'
        
        print(f"\nNavigating to {url}...")
        driver.get(url)
        
        # Wait for main content to load
        print("\nWaiting for page content to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Let the page fully render and handle any JavaScript
        time.sleep(5)
        
        print("\nPage Title:", driver.title)
        print("\nCurrent URL:", driver.current_url)
        
        # Get page source and cookies
        print("\nCookies:", json.dumps(driver.get_cookies(), indent=2))
        
        # Check for specific elements
        try:
            product_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component='ProductTitle']"))
            )
            print("\nProduct Name:", product_name.text)
        except Exception as e:
            print("\nCouldn't find product name:", str(e))
        
        # Print page source preview
        print("\nPage Source Preview (first 1000 characters):")
        print(driver.page_source[:1000])
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    finally:
        try:
            driver.quit()
            print("\nBrowser closed successfully")
        except:
            print("\nError closing browser")

if __name__ == "__main__":
    test_stockx_selenium()

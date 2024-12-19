import requests
import json
import time

def test_stockx_access():
    url = 'https://stockx.com/air-jordan-1-retro-low-og-sp-travis-scott-olive-w'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # Create a session to maintain cookies
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        print("\nMaking request to StockX...")
        response = session.get(url)
        
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
            
        print("\nResponse Content Preview:")
        content = response.text[:1000]
        print(content)
        
        if response.status_code == 403:
            print("\nAccess Forbidden (403) - This might indicate:")
            print("1. IP being blocked")
            print("2. Anti-bot protection")
            print("3. Missing required headers/cookies")
            
    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    test_stockx_access()

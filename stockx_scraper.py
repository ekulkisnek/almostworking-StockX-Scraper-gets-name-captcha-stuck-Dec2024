import requests
import json
import time

class StockXScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'X-Algolia-API-Key': '6b5e76b49705eb9f51a06d3c82f7acee',
            'X-Algolia-Application-Id': 'XW7SBCT9V6'
        }
        
    def search_product(self, query):
        try:
            params = {
                "params": f"query={query}&hitsPerPage=1"
            }
            
            response = requests.post(
                'https://xw7sbct9v6-1.algolianet.com/1/indexes/products/query',
                headers=self.headers,
                json=params
            )
            
            if response.status_code != 200:
                print(f"Search API Error - Status Code: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None
                
            data = response.json()
            if not data.get('hits'):
                print("No results found")
                return None
                
            product = data['hits'][0]
            return {
                'name': product['name'],
                'style_id': product['style_id'],
                'url_key': product['url'],
                'uuid': product.get('uuid'),
                'lowest_ask': product.get('lowest_ask'),
                'retail_price': product.get('searchable_traits', {}).get('Retail Price'),
                'release_date': product.get('release_date'),
                'brand': product.get('brand'),
                'colorway': product.get('colorway'),
            }
        except Exception as e:
            print(f"Error searching product: {e}")
            return None
    
    def get_prices(self, url_key):
        try:
            # Updated headers to better mimic a browser request
            product_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://stockx.com/',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Add a small delay to avoid rate limiting
            time.sleep(2)
            
            # Add a small delay to avoid rate limiting
            time.sleep(2)
            
            # Make initial request to get session cookies
            session = requests.Session()
            session.headers.update(product_headers)
            
            print("\nMaking initial request to StockX...")
            initial_response = session.get(f'https://stockx.com/{url_key}')
            print(f"Initial request status code: {initial_response.status_code}")
            
            # Update session headers for API request
            session.headers.update({
                'Accept': 'application/json',
                'x-requested-with': 'XMLHttpRequest',
                'sec-fetch-mode': 'cors'
            })
            
            print("\nMaking API request...")
            for attempt in range(3):  # Try up to 3 times
                response = session.get(
                    f'https://stockx.com/api/products/{url_key}?includes=market,variants&currency=USD&country=US'
                )
                if response.status_code == 200:
                    break
                print(f"Attempt {attempt + 1} failed with status code {response.status_code}")
                time.sleep(2)  # Wait before retrying
            
            if response.status_code != 200:
                print(f"Product API Error - Status Code: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                print("\nFailed to decode JSON response")
                print("Response Headers:", dict(response.headers))
                print("Response Status:", response.status_code)
                print("Response Text Preview:", response.text[:1000])
                return None
                
            print("\nSuccessfully decoded JSON response")
            if isinstance(data, dict):
                print("Response Keys:", list(data.keys()))
                if 'Product' in data:
                    print("Found 'Product' key in response")
                    print("Product Keys:", list(data['Product'].keys()))
                elif 'product' in data:
                    print("Found 'product' key in response")
                    print("product Keys:", list(data['product'].keys()))
                else:
                    print("Neither 'Product' nor 'product' key found in response")
                
            print("\nAPI Response Structure:")
            print("Status Code:", response.status_code)
            print("Headers:", dict(response.headers))
            print("Available Keys:", list(data.keys()) if isinstance(data, dict) else "Not a dictionary")
            
            if isinstance(data, dict):
                print("\nDetailed Response Structure:")
                if 'Product' in data:
                    print("Product Keys:", list(data['Product'].keys()))
                elif 'product' in data:
                    print("product Keys:", list(data['product'].keys()))
                print("Response Preview:", json.dumps(data, indent=2)[:500])
            
            # Try various known response structures
            product_data = None
            if isinstance(data, dict):
                product_data = (data.get('Product') or 
                              data.get('product') or 
                              data.get('data', {}).get('product'))
            
            if not product_data:
                print("Could not find product data in response")
                return None
            
            # Try to get variants/market data
            variants = []
            
            # Check different possible locations for variant data
            if 'variants' in product_data:
                variants = product_data['variants']
            elif 'children' in product_data:
                variants = list(product_data['children'].values())
            elif 'market' in product_data:
                market_data = product_data['market']
                if 'variants' in market_data:
                    variants = market_data['variants']
                    
            if not variants:
                print("No variant data found in response")
                print("Available keys in product_data:", list(product_data.keys()))
                return None
            
            prices = {}
            # Ensure variants is a list
            if isinstance(variants, dict):
                variants = list(variants.values())
            
            for variant in variants:
                if not isinstance(variant, dict):
                    continue
                    
                # Try different possible size fields
                size = None
                for size_key in ['shoeSize', 'size', 'sizeKey', 'sizeLabel']:
                    if size_key in variant:
                        size = str(variant[size_key])
                        break
                
                if not size:
                    continue
                    
                # Get market data
                market = variant.get('market', {})
                if not isinstance(market, dict):
                    continue
                
                asks = market.get('lowestAsk') or market.get('lowest_ask')
                bids = market.get('highestBid') or market.get('highest_bid')
                sales = market.get('lastSale') or market.get('last_sale')
                
                if any([asks, bids, sales]):
                    prices[size] = {
                        'lowest_ask': asks if asks else 'No asks',
                        'highest_bid': bids if bids else 'No bids',
                        'last_sale': sales if sales else 'No sales'
                    }
            
            return prices
        except Exception as e:
            print(f"Error getting prices: {e}")
            if 'response' in locals():
                print(f"Status code: {response.status_code}")
                print(f"Response text: {response.text[:500]}")
            return None

def main():
    scraper = StockXScraper()
    
    while True:
        try:
            # Get user input
            query = input("\nEnter shoe name (or 'quit' to exit): ")
            
            if query.lower() == 'quit':
                break
            
            # Search for product
            print("\nSearching for product...")
            product = scraper.search_product(query)
            if not product:
                print("Product not found")
                continue
                
            print("\nProduct found:")
            print(f"Name: {product['name']}")
            print(f"Style ID: {product['style_id']}")
            print(f"Retail Price: ${product['retail_price']}")
            print(f"Brand: {product['brand']}")
            print(f"Colorway: {product['colorway']}")
            
            # Get prices for all sizes
            print("\nFetching prices...")
            prices = scraper.get_prices(product['url_key'])
            if not prices:
                print("Could not get prices")
                continue
                
            print("\nPrices by size:")
            for size, price_data in prices.items():
                print(f"\nSize {size}:")
                print(f"Lowest Ask: ${price_data['lowest_ask']}")
                print(f"Highest Bid: ${price_data['highest_bid']}")
                print(f"Last Sale: ${price_data['last_sale']}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()

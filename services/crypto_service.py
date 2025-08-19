import requests
from config.settings import COINGECKO_BASE_URL
from config.coins import COINS

class CryptoService:
    def __init__(self):
        self.base_url = COINGECKO_BASE_URL
    
    def get_coin_prices(self):
        """Tüm coinlerin fiyat ve 24h değişim verilerini çek"""
        coin_ids = ','.join(COINS.keys())
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': coin_ids,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_market_cap': 'true'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Fiyat verisi çekme hatası: {e}")
            return {}
    
    def get_trending_coins(self):
        """Trending coinleri çek"""
        url = f"{self.base_url}/search/trending"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json().get('coins', [])
        except Exception as e:
            print(f"Trending verisi çekme hatası: {e}")
            return []
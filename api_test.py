from services.crypto_service import CryptoService
from services.reddit_service import RedditService

print('🔍 CoinGecko API test...')
crypto = CryptoService()
prices = crypto.get_coin_prices()
print(f'✅ {len(prices)} coin fiyatı alındı')

if prices:
    first_coin = list(prices.keys())[0]
    print(f'Örnek: {first_coin} = ${prices[first_coin]["usd"]}')

print('\n🔍 Reddit API test...')
reddit = RedditService()
mentions = reddit.get_coin_mentions(limit=10)
print(f'✅ Reddit mentions: {mentions}')
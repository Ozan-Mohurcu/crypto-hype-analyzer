import os

# Reddit API
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', 'PZNHmWz1xNgmUCX_WFUh5g')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', 'bT18AscWcgmoCb3khT0ISV6ihnOFvg')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'HypeCoinDailyBot/0.1 by Other-Confidence7785')

# Twitter API
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', '5QSzoLcsWhfeNU9jYtYHckCrPFIlZfEHRj8w3Mt0v8edZWEHjg')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET', 'C0A_OJ348VqgkrgYQiKm_u8yJ1BsxM5ZVY1a6kAeRyRP6YrAZ_')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '1957744993927323648-6byA09QyBky4FeuKcIyqE3xoluIps5')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET', 'prMkDbYvVP5vzNxLv9XT6FUbwvPMZx9nYAYiOTZ7NSOzL')

# CoinGecko API
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Tweet ayarları
TWEET_SCHEDULE = [9, 12, 15, 18, 21]  # Türkiye saati - günde 5 tweet
import praw
from config.settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from config.coins import COINS, SUBREDDITS

class RedditService:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    
    def get_coin_mentions(self, limit=50):
        """Reddit'ten coin mentions sayısını al"""
        mentions = {coin_id: 0 for coin_id in COINS.keys()}
        
        for subreddit_name in SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Hot posts'ları kontrol et
                for post in subreddit.hot(limit=limit):
                    title_lower = post.title.lower()
                    content_lower = getattr(post, 'selftext', '').lower()
                    
                    for coin_id, symbol in COINS.items():
                        # Coin adı veya sembolünü ara
                        coin_name = coin_id.replace('-', ' ')
                        if (coin_name in title_lower or 
                            symbol.lower() in title_lower or
                            coin_name in content_lower or 
                            symbol.lower() in content_lower):
                            
                            # Upvote oranına göre ağırlıklandır
                            weight = min(post.score / 100, 5)  # Max 5x weight
                            mentions[coin_id] += weight
                            
            except Exception as e:
                print(f"Reddit subreddit {subreddit_name} hatası: {e}")
                continue
        
        return mentions
    
    def get_sentiment_score(self, coin_id, limit=20):
        """Belirli bir coin için sentiment skoru"""
        positive_words = ['moon', 'bullish', 'buy', 'pump', 'hodl', 'diamond', 'rocket']
        negative_words = ['dump', 'crash', 'bearish', 'sell', 'dead', 'scam']
        
        sentiment_score = 0
        
        try:
            # r/CryptoCurrency'de coin arama
            subreddit = self.reddit.subreddit('CryptoCurrency')
            coin_name = coin_id.replace('-', ' ')
            
            for post in subreddit.search(coin_name, limit=limit, time_filter='day'):
                text = (post.title + ' ' + getattr(post, 'selftext', '')).lower()
                
                for word in positive_words:
                    sentiment_score += text.count(word) * 2
                
                for word in negative_words:
                    sentiment_score -= text.count(word) * 1
                    
        except Exception as e:
            print(f"Sentiment analizi hatası: {e}")
        
        return max(0, sentiment_score)  # Negatif olmayacak şekilde
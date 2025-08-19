import tweepy
import os
from config.settings import (
    TWITTER_API_KEY, TWITTER_API_SECRET, 
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)

class TwitterService:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        
        # v1.1 API for media upload
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY, TWITTER_API_SECRET,
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
        )
        self.api = tweepy.API(auth)
    
    def post_tweet_with_media(self, text, image_path):
        """Tweet + görsel paylaş"""
        try:
            # Görseli yükle
            media = self.api.media_upload(image_path)
            
            # Tweet at
            tweet = self.client.create_tweet(
                text=text,
                media_ids=[media.media_id]
            )
            
            print(f"Tweet gönderildi: {tweet.data['id']}")
            return tweet.data['id']
            
        except Exception as e:
            print(f"Tweet gönderme hatası: {e}")
            return None
    
    def format_tweet_text(self, coin_data, hype_score):
        """Tweet metnini formatla"""
        coin_id = coin_data['coin_id']
        symbol = coin_data['symbol']
        price = coin_data['price']
        change_24h = coin_data['change_24h']
        reddit_mentions = coin_data['reddit_mentions']
        
        # Emoji seç
        emoji = "🚀" if change_24h > 0 else "📉" if change_24h < -5 else "📊"
        
        # Değişim formatla
        change_text = f"+{change_24h:.1f}%" if change_24h > 0 else f"{change_24h:.1f}%"
        
        text = f"""{emoji} {symbol} Hype Analizi

💰 Fiyat: ${price:,.2f} ({change_text})
🔥 Reddit Hype: {reddit_mentions:.0f} mentions
📊 Hype Skoru: {hype_score:.1f}/10

#Crypto #{symbol} #HypeCoinDaily #Bitcoin"""
        
        return text
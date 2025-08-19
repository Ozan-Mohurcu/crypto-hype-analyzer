from config.coins import COINS

class DataProcessor:
    def calculate_hype_score(self, price_data, reddit_data, sentiment_data):
        """Hype skorunu hesapla"""
        scores = {}
        
        for coin_id in COINS.keys():
            if coin_id not in price_data:
                continue
                
            # Fiyat değişimi (24h)
            price_change = price_data[coin_id].get('usd_24h_change', 0)
            
            # Reddit mentions
            reddit_mentions = reddit_data.get(coin_id, 0)
            
            # Sentiment skoru
            sentiment = sentiment_data.get(coin_id, 0)
            
            # Hype skoru hesapla (0-10 arası)
            # %30 fiyat değişimi, %40 reddit mentions, %30 sentiment
            normalized_price = min(max(price_change / 10, -3), 3)  # -3 ile 3 arası
            normalized_reddit = min(reddit_mentions / 10, 5)  # Max 5
            normalized_sentiment = min(sentiment / 20, 2)  # Max 2
            
            hype_score = (
                normalized_price * 0.3 + 
                normalized_reddit * 0.4 + 
                normalized_sentiment * 0.3
            ) + 5  # Base 5 puan
            
            # 0-10 arası sınırla
            hype_score = max(0, min(10, hype_score))
            
            scores[coin_id] = {
                'hype_score': hype_score,
                'price': price_data[coin_id]['usd'],
                'change_24h': price_change,
                'reddit_mentions': reddit_mentions,
                'sentiment': sentiment,
                'symbol': COINS[coin_id],
                'coin_id': coin_id
            }
        
        return scores
    
    def get_top_hype_coin(self, scores):
        """En yüksek hype skoruna sahip coini bul"""
        if not scores:
            return None
            
        top_coin = max(scores.items(), key=lambda x: x[1]['hype_score'])
        return top_coin[1]
import json
import datetime
from config.settings import TWEET_SCHEDULE
from services.crypto_service import CryptoService
from services.reddit_service import RedditService
from services.twitter_service import TwitterService
from utils.data_processor import DataProcessor
from utils.chart_generator import ChartGenerator

def lambda_handler(event, context):
    """AWS Lambda ana fonksiyonu"""
    
    # Saat kontrolü (Türkiye saati)
    current_hour = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).hour
    
    if current_hour not in TWEET_SCHEDULE:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Zamanlanmış saat değil. Şu an: {current_hour}, Zamanlar: {TWEET_SCHEDULE}'
            })
        }
    
    try:
        # Servisleri başlat
        crypto_service = CryptoService()
        reddit_service = RedditService()
        twitter_service = TwitterService()
        data_processor = DataProcessor()
        chart_generator = ChartGenerator()
        
        print("Veri toplama başlatılıyor...")
        
        # 1. Crypto verileri çek
        price_data = crypto_service.get_coin_prices()
        print(f"Fiyat verisi alındı: {len(price_data)} coin")
        
        # 2. Reddit hype verisi çek
        reddit_mentions = reddit_service.get_coin_mentions()
        print(f"Reddit mentions alındı: {reddit_mentions}")
        
        # 3. Sentiment analizi yap (en popüler 3 coin için)
        top_mentioned = sorted(reddit_mentions.items(), 
                              key=lambda x: x[1], reverse=True)[:3]
        
        sentiment_data = {}
        for coin_id, _ in top_mentioned:
            sentiment_data[coin_id] = reddit_service.get_sentiment_score(coin_id)
        
        print(f"Sentiment analizi tamamlandı: {sentiment_data}")
        
        # 4. Hype skorlarını hesapla
        hype_scores = data_processor.calculate_hype_score(
            price_data, reddit_mentions, sentiment_data
        )
        print(f"Hype skorları hesaplandı: {len(hype_scores)} coin")
        
        # 5. En yüksek hype coin'i bul
        top_coin = data_processor.get_top_hype_coin(hype_scores)
        
        if not top_coin:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Top coin bulunamadı'})
            }
        
        print(f"Top coin: {top_coin['symbol']} - Skor: {top_coin['hype_score']:.1f}")
        
        # 6. Chart oluştur
        chart_path = chart_generator.create_hype_chart(top_coin)
        print(f"Chart oluşturuldu: {chart_path}")
        
        # 7. Tweet gönder
        tweet_text = twitter_service.format_tweet_text(top_coin, top_coin['hype_score'])
        tweet_id = twitter_service.post_tweet_with_media(tweet_text, chart_path)
        
        if tweet_id:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Tweet başarıyla gönderildi',
                    'tweet_id': tweet_id,
                    'coin': top_coin['symbol'],
                    'hype_score': top_coin['hype_score'],
                    'hour': current_hour
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Tweet gönderilemedi'})
            }
            
    except Exception as e:
        print(f"Lambda hatası: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Lokal test için
if __name__ == "__main__":
    result = lambda_handler({}, {})
    print(json.dumps(result, indent=2))
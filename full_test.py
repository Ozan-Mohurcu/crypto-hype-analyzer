from services.crypto_service import CryptoService
from services.reddit_service import RedditService
from utils.data_processor import DataProcessor
from utils.chart_generator import ChartGenerator

print('🚀 Tam sistem testi başlatılıyor...')

# 1. Verileri topla
crypto = CryptoService()
reddit = RedditService()
processor = DataProcessor()
chart_gen = ChartGenerator()

print('📊 Veri toplama...')
prices = crypto.get_coin_prices()
mentions = reddit.get_coin_mentions(limit=20)

print('🧮 Hype skorları hesaplanıyor...')
# Basit sentiment (şimdilik boş)
sentiment = {coin: 5 for coin in mentions.keys()}

hype_scores = processor.calculate_hype_score(prices, mentions, sentiment)

print('🏆 Top coin seçiliyor...')
top_coin = processor.get_top_hype_coin(hype_scores)

if top_coin:
    print(f'✅ Kazanan: {top_coin["symbol"]} - Skor: {top_coin["hype_score"]:.1f}')
    print(f'   Fiyat: ${top_coin["price"]:.2f}')
    print(f'   24h değişim: {top_coin["change_24h"]:.1f}%')
    print(f'   Reddit mentions: {top_coin["reddit_mentions"]:.1f}')
    
    print('📈 Grafik oluşturuluyor...')
    chart_path = chart_gen.create_hype_chart(top_coin)
    print(f'✅ Grafik kaydedildi: {chart_path}')
    
    print('🎯 Sistem testi BAŞARILI!')
else:
    print('❌ Top coin bulunamadı')
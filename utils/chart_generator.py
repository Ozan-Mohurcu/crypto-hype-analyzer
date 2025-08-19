import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from datetime import datetime
import os

# Dark theme ayarları
plt.style.use('dark_background')
sns.set_palette("deep")

class ChartGenerator:
    def __init__(self):
        self.colors = {
            'background': '#1E1E1E',
            'primary': '#8B0000',  # Koyu kırmızı
            'secondary': '#A0A0A0',  # Gri
            'text': '#FFFFFF',
            'grid': '#333333'
        }
    
    def create_hype_chart(self, coin_data):
        """Hype chart oluştur"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), 
                                       facecolor=self.colors['background'])
        
        # Üst grafik - Hype Score
        categories = ['Fiyat\nDeğişimi', 'Reddit\nHype', 'Sentiment', 'TOPLAM\nHYPE']
        values = [
            min(max(coin_data['change_24h'] / 10 * 3, 0), 3),
            min(coin_data['reddit_mentions'] / 10 * 4, 4), 
            min(coin_data['sentiment'] / 20 * 3, 3),
            coin_data['hype_score']
        ]
        
        bars = ax1.bar(categories, values, 
                      color=[self.colors['secondary'], self.colors['secondary'], 
                            self.colors['secondary'], self.colors['primary']],
                      alpha=0.8, edgecolor='white', linewidth=1)
        
        ax1.set_title(f"{coin_data['symbol']} Hype Analizi", 
                     fontsize=16, color=self.colors['text'], 
                     fontweight='bold', pad=20)
        ax1.set_ylabel('Skor', fontsize=12, color=self.colors['text'])
        ax1.set_ylim(0, 10)
        ax1.grid(True, alpha=0.3, color=self.colors['grid'])
        
        # Bar değerlerini göster
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value:.1f}', ha='center', va='bottom',
                    color=self.colors['text'], fontweight='bold')
        
        # Alt grafik - Fiyat trend simülasyonu (daha gerçekçi)
        x = np.linspace(0, 24, 25)
        base_price = coin_data['price']
        
        # Gerçekçi fiyat volatilitesi
        volatility = max(abs(coin_data['change_24h']) / 100, 0.02)  # Min %2 volatilite
        price_changes = np.random.normal(0, volatility, 24)
        
        # Kümülatif değişim + trend
        trend_factor = coin_data['change_24h'] / 100 / 24  # Günlük trendin saatlik dağılımı
        cumulative_changes = np.cumsum(price_changes) + np.linspace(0, coin_data['change_24h']/100, 24)
        
        # Son 24 saatin simülasyonu
        prices = []
        for i in range(25):
            if i == 0:
                prices.append(base_price / (1 + coin_data['change_24h']/100))  # 24 saat önceki fiyat
            else:
                prices.append(prices[0] * (1 + cumulative_changes[i-1]))
        
        ax2.plot(x, prices, color=self.colors['primary'], linewidth=3, alpha=0.8)
        ax2.fill_between(x, prices, alpha=0.2, color=self.colors['primary'])
        
        # Y eksenini daha iyi ayarla
        price_min = min(prices) * 0.999
        price_max = max(prices) * 1.001
        ax2.set_ylim(price_min, price_max)
        
        # Daha iyi formatlama
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax2.set_xticks([0, 6, 12, 18, 24])
        ax2.set_xticklabels(['24h ago', '18h ago', '12h ago', '6h ago', 'Now'])
        
        ax2.set_title('24 Saatlik Fiyat Trendi', fontsize=14, 
                     color=self.colors['text'], fontweight='bold')
        ax2.set_xlabel('Saat', fontsize=12, color=self.colors['text'])
        ax2.set_ylabel('Fiyat ($)', fontsize=12, color=self.colors['text'])
        ax2.grid(True, alpha=0.3, color=self.colors['grid'])
        
        # Watermark ekle
        fig.text(0.95, 0.02, 'Created by Ozan M', 
                fontsize=10, color=self.colors['secondary'], 
                ha='right', alpha=0.7, style='italic')
        
        plt.tight_layout()
        
        # Windows ve Lambda uyumlu dosya yolu
        if os.name == 'nt':  # Windows
            chart_path = f"{coin_data['symbol']}_hype_chart.png"
        else:  # Linux/Lambda
            chart_path = f"/tmp/{coin_data['symbol']}_hype_chart.png"
            
        plt.savefig(chart_path, dpi=150, facecolor=self.colors['background'],
                   bbox_inches='tight', edgecolor='none')
        plt.close()
        
        return chart_path
    
    def create_simple_chart(self, coin_data):
        """Basit bar chart (alternatif)"""
        fig, ax = plt.subplots(figsize=(8, 6), facecolor=self.colors['background'])
        
        ax.bar(['Hype Score'], [coin_data['hype_score']], 
               color=self.colors['primary'], alpha=0.8, width=0.5)
        
        ax.set_title(f"{coin_data['symbol']} Hype Skoru: {coin_data['hype_score']:.1f}/10", 
                    fontsize=16, color=self.colors['text'], fontweight='bold')
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3, color=self.colors['grid'])
        
        # Watermark
        fig.text(0.95, 0.02, 'Created by Ozan M', 
                fontsize=10, color=self.colors['secondary'], 
                ha='right', alpha=0.7, style='italic')
        
        plt.tight_layout()
        
        # Windows ve Lambda uyumlu dosya yolu
        if os.name == 'nt':  # Windows
            chart_path = f"{coin_data['symbol']}_simple_chart.png"
        else:  # Linux/Lambda
            chart_path = f"/tmp/{coin_data['symbol']}_simple_chart.png"
            
        plt.savefig(chart_path, dpi=150, facecolor=self.colors['background'],
                   bbox_inches='tight', edgecolor='none')
        plt.close()
        
        return chart_path
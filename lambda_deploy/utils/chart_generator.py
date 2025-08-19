import os

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    HAS_PLOTTING = True
except ImportError:
    HAS_PLOTTING = False
    print("Using PIL for basic charts")

class ChartGenerator:
    def __init__(self):
        self.colors = {
            'background': '#1E1E1E',
            'primary': '#8B0000',
            'secondary': '#A0A0A0',
            'text': '#FFFFFF'
        }
    
    def create_hype_chart(self, coin_data):
        """Hype chart oluştur"""
        if HAS_PLOTTING:
            # Matplotlib kodunu buraya koy (önceki tam kod)
            pass
        else:
            # PIL yok, text dosyası oluştur
            return self._create_text_fallback(coin_data)
    
    def _create_text_fallback(self, coin_data):
        """Text dosyası oluştur"""
        text_content = f"""
{coin_data['symbol']} Hype Report
====================
Price: ${coin_data['price']:.2f}
24h Change: {coin_data['change_24h']:.1f}%
Reddit Mentions: {coin_data['reddit_mentions']:.1f}
Hype Score: {coin_data['hype_score']:.1f}/10

Created by Ozan M
"""
        
        if os.name == 'nt':
            file_path = f"{coin_data['symbol']}_report.txt"
        else:
            file_path = f"/tmp/{coin_data['symbol']}_report.txt"
        
        with open(file_path, 'w') as f:
            f.write(text_content)
        
        return file_path
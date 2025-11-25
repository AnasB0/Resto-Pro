# 🍽️ Restaurant AI Dashboard

A modern, user-friendly AI-powered dashboard for restaurant insights powered by Streamlit, OpenRouter LLM, and statistical analysis.

## ✨ Features

### 📊 Dashboard Overview
- Real-time restaurant performance metrics
- Customer sentiment analysis (Positive/Negative/Neutral)
- Most talked-about dishes visualization
- Sales summary and happy customer percentage

### 🏆 Dish Performance Analysis
- Overall performance scoring (sentiment + popularity + sales)
- Individual dish happiness ratings
- Sales volume correlations
- Color-coded performance rankings (Red-Yellow-Green)

### 📦 Inventory Management
- Real-time stock level monitoring
- Automated inventory alerts:
  - 🚨 Critical: Less than 3 days of stock
  - ⚠️ Warning: 3-7 days of stock
  - ✅ Good: 7+ days of stock
- Days-remaining calculation based on sales velocity
- Stock visualization charts

### 📈 Sales Forecasting
- 14-day sales predictions using ARIMA
- Trend analysis (upward/downward/stable)
- Historical vs. predicted sales comparison
- Action recommendations based on forecast

### 🔍 Review Analysis
- Browse customer reviews by sentiment filter
- AI-powered review summaries via OpenRouter LLM
- Review text analysis and pattern detection
- Source tracking (Google, Yelp, TripAdvisor, etc.)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/restaurant-ai-dashboard.git
cd restaurant-ai-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download spaCy model** (required for NLP)
```bash
python -m spacy download en_core_web_sm
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
COLAB_API_URL=https://your-ngrok-url/
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

5. **Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
restaurant-ai-dashboard/
├── app.py                 # Main Streamlit application
├── colab_server.py        # Optional Colab backend server
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (DO NOT commit)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── FEATURES.md           # Detailed feature documentation
└── data/
    ├── restaurant_reviews.csv    # Customer reviews
    ├── pos_sales.csv             # Sales transaction data
    ├── inventory.csv             # Stock levels
    └── mapped_reviews_export.csv # Reviews mapped to dishes
```

## 📊 Data Format

### restaurant_reviews.csv
```csv
date,review_text,rating,source
2025-11-20,The Margherita Pizza was absolutely delicious!,5,Google Reviews
```

### pos_sales.csv
```csv
item,qty,price,date
Margherita Pizza,5,9.99,2025-11-20
```

### inventory.csv
```csv
sku,item,qty_on_hand,unit_cost
SKU001,Margherita Pizza,35,3.50
```

## 🤖 AI Features

### OpenRouter LLM Integration
- Summarizes customer reviews automatically
- Extracts insights and patterns
- Provides actionable recommendations
- Uses GPT-4o-mini for cost-effective analysis

### Sentiment Analysis
- TextBlob for basic sentiment scoring (-1 to +1)
- Categorizes reviews as Positive/Negative/Neutral
- Dish-level sentiment aggregation

### Sales Forecasting
- ARIMA(1,1,1) time series model
- Predicts 14-day sales trends
- Handles seasonality automatically

### NLP Processing
- spaCy for entity recognition
- Dish extraction from review text
- Noun chunk analysis

## 🔧 Configuration

### Environment Variables
- `COLAB_API_URL`: ngrok public URL for Colab backend
- `OPENROUTER_API_KEY`: API key for LLM access
- `OPENROUTER_MODEL`: Model identifier (default: openai/gpt-4o-mini)

### Streamlit Settings
Edit `.streamlit/config.toml` to customize:
- Theme (light/dark)
- Page width
- Font size
- Color scheme

## 📦 Dependencies

Core packages:
- **streamlit** - Dashboard framework
- **pandas** - Data manipulation
- **plotly** - Interactive visualizations
- **textblob** - Sentiment analysis
- **spacy** - NLP processing
- **statsmodels** - Time series forecasting
- **requests** - HTTP client for APIs
- **flask** - Backend server (optional)
- **python-dotenv** - Environment variable management

See `requirements.txt` for complete list.

## 🎨 UI/UX Features

- **Emoji indicators** for quick status scanning (😊 🚨 ⭐ 📈)
- **Color-coded alerts** (🔴 Red = Critical, 🟡 Yellow = Warning, 🟢 Green = Good)
- **Helpful explanations** for non-technical users
- **Interactive charts** with hover details
- **Responsive design** that works on all screen sizes
- **Tab-based navigation** for organized information

## 🔐 Security

- API keys stored in `.env` (excluded from git)
- `.gitignore` prevents accidental commits of sensitive data
- No hardcoded credentials in code
- Environment variable based configuration

## 📈 Performance Metrics

Dashboard calculates:
- **Sentiment Score**: Customer happiness (-1 to +1)
- **Performance Score**: Weighted combination of sentiment, popularity, sales (0-100)
- **Days on Hand**: Stock duration based on sales velocity
- **Sales Trend**: Percentage change in predicted vs. historical sales

## 🐛 Troubleshooting

### CSV Parsing Error
- Ensure CSV files have consistent column counts
- Check for extra commas in text fields (use quotes)
- Validate file encoding (UTF-8 recommended)

### statsmodels Import Error
```bash
pip install --upgrade statsmodels
```

### spaCy Model Not Found
```bash
python -m spacy download en_core_web_sm
```

### App Won't Start
```bash
# Clear cache and restart
rm -rf .streamlit/
streamlit run app.py
```

## 📝 Usage Examples

### Viewing Performance Dashboard
1. Open the app and go to **"🏆 Dish Performance"** tab
2. See which dishes are your stars (green = excellent)
3. Identify underperformers (red = needs improvement)

### Checking Inventory
1. Go to **"📦 Inventory"** tab
2. Red alerts = reorder immediately
3. Yellow alerts = plan reorder soon
4. Green = sufficient stock

### Forecasting Sales
1. Go to **"📈 Forecasting"** tab
2. View 14-day prediction
3. Plan staffing based on predicted demand
4. Prepare inventory for high-demand periods

### Analyzing Reviews
1. Go to **"🔍 Reviews"** tab
2. Filter by sentiment (😊 😟 😐)
3. Click "Generate AI Insights" for summary
4. Get actionable recommendations

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📧 Contact & Support

- **Author**: Anas
- **Email**: anas@example.com
- **Issues**: Report via GitHub Issues
- **Discussions**: GitHub Discussions

## 🙏 Acknowledgments

- Streamlit for the amazing dashboard framework
- OpenRouter for LLM API access
- spaCy for NLP capabilities
- Plotly for interactive visualizations
- The open-source community

## 🗓️ Changelog

### v1.0.0 (November 25, 2025)
- ✅ Initial release
- ✅ Complete dashboard with 5 tabs
- ✅ AI-powered insights
- ✅ Sales forecasting
- ✅ Inventory alerts
- ✅ User-friendly UI for non-technical users

---

**Made with ❤️ for restaurant owners and managers**

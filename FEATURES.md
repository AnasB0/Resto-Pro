# 🍽️ Restaurant AI Dashboard - Features Overview

## ✨ New Features Implemented

### 1. **Auto Charts (Plotly)**
   - Interactive sentiment distribution (pie chart)
   - Top dishes visualization (horizontal bar chart)
   - Dish performance rankings with color gradients
   - Sentiment vs Sales scatter plots with hover data
   - Stock level visualization

### 2. **Dish Performance Ranking**
   - **Overall Score**: Weighted combination of sentiment, popularity, and sales
   - **Metrics Per Dish**:
     - Average Sentiment Score
     - Review Count
     - Positive Review Count
     - Total Quantity Sold
     - Average Price
   - **Scoring Formula**:
     - Sentiment Score: 40%
     - Popularity (review count): 30%
     - Sales Volume: 30%

### 3. **Inventory Alerts**
   - 🚨 **Critical Alert** (Red): Items with < 3 days of stock
   - ⚠️ **Warning Alert** (Yellow): Items with 3-7 days of stock
   - ℹ️ **Info Alert** (Blue): Overstock situations (>30 days)
   - Dynamic calculation based on daily sales velocity
   - Color-coded alert system for quick visual scanning

### 4. **Sales Forecasting (ARIMA)**
   - Lightweight ARIMA(1,1,1) model
   - 14-day sales forecast with historical comparison
   - Trend analysis (📈 Upward / 📉 Downward)
   - Visual forecast overlay on historical data
   - Automatic handling of insufficient data

### 5. **Modern UI Upgrade**
   - **5-Tab Dashboard Layout**:
     1. 📊 Overview - Key metrics and sentiment distribution
     2. 🏆 Dish Performance - Ranking and analysis
     3. 📦 Inventory - Alerts and stock visualization
     4. 📈 Forecasting - Sales predictions
     5. 🔍 Reviews - Raw review data and LLM summary
   
   - **Visual Enhancements**:
     - Gradient color schemes (Plotly viridis)
     - Interactive charts with hover details
     - Custom CSS styling with modern colors
     - Wide layout for better data visualization
     - Metric cards for KPIs
     - Alert cards with color-coded borders

## 📊 Dashboard Metrics

### Overview Tab
- Total Reviews Count
- Average Sentiment Score
- Positive Reviews Percentage
- Total Items Sold

### Dish Performance Tab
- Interactive ranking table
- Performance score visualization
- Sentiment vs Sales correlation plot

### Inventory Tab
- Real-time stock alerts
- Stock level bar chart
- Days remaining calculation

### Forecasting Tab
- 14-day sales forecast
- Historical vs Forecasted comparison
- Trend indicator
- Confidence metrics

### Reviews Tab
- Full review data table
- AI-powered summary generation (OpenRouter LLM)
- Sentiment analysis per review

## 🔧 Technical Stack

- **Frontend**: Streamlit
- **Charting**: Plotly (interactive, responsive)
- **Time Series**: ARIMA (statsmodels)
- **NLP**: spaCy + TextBlob
- **LLM**: OpenRouter (gpt-4o-mini)
- **Data Processing**: Pandas, NumPy

## 📁 Data Source

Auto-loads from `/data` folder:
- `restaurant_reviews.csv` - Review data with `review_text` column
- `pos_sales.csv` - Sales data with `item`, `qty`, `price`, `date`
- `inventory.csv` - Stock data with `item`, `qty_on_hand`
- `mapped_reviews_export.csv` - Alternative review format with `text` column

## 🚀 Running the App

```bash
cd /mnt/d/coursesP/Resto
streamlit run app.py
```

Access at: http://localhost:8502

## 📦 Dependencies

See `requirements.txt` for full list. Key packages:
- streamlit >= 1.20
- plotly >= 5.0
- statsmodels >= 0.14
- pandas >= 1.5
- spacy >= 3.0
- textblob >= 0.17

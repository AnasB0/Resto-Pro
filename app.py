import streamlit as st
import pandas as pd
import requests
import spacy
from textblob import TextBlob
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import warnings
import subprocess
import sys
warnings.filterwarnings('ignore')

# ----------------------------------------------------------
# Load spaCy model with graceful fallback
# ----------------------------------------------------------
NLP_AVAILABLE = False
nlp = None

try:
    nlp = spacy.load("en_core_web_sm")
    NLP_AVAILABLE = True
except OSError:
    # spaCy model not available - app will work without NLP features
    NLP_AVAILABLE = False
    st.warning("""
    ⚠️ **Language Model Initializing**
    
    The spaCy model is downloading in the background. 
    The app is ready to use, but advanced text analysis may take a moment.
    
    **Next steps:**
    1. Click "Manage app" (bottom right)
    2. Click "Reboot app"
    3. Wait 10 minutes for full restart
    
    For faster results, you can redeploy from GitHub.
    """)

# Try to import statsmodels, but make it optional
try:
    from statsmodels.tsa.arima.model import ARIMA
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False
    ARIMA = None

# ----------------------------------------------------------
# HARD-CODED API KEY (as you requested)
# ----------------------------------------------------------
OPENROUTER_API_KEY = "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"

# ----------------------------------------------------------
# Configure Streamlit
# ----------------------------------------------------------
st.set_page_config(page_title="Restaurant AI Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .alert-danger {
        background-color: #fee;
        border-left: 4px solid #f44;
        padding: 1rem;
        border-radius: 5px;
    }
    .alert-warning {
        background-color: #fef3cd;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
    }
    .alert-success {
        background-color: #e6f7ed;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .explanation {
        font-size: 0.9em;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# Helper: User-friendly explanations
# ----------------------------------------------------------
EXPLANATIONS = {
    "sentiment": "📊 Sentiment shows how happy or unhappy customers are. Positive = Happy customer, Negative = Unhappy customer.",
    "performance": "🏆 Performance Score combines customer satisfaction, popularity, and sales. Higher score = Better overall dish.",
    "inventory": "📦 Inventory shows how much stock you have and how long it will last based on recent sales.",
    "forecast": "📈 Forecast predicts how many items you'll sell in the next 2 weeks based on past sales patterns.",
    "alert": "🚨 Alerts warn you about potential stock issues so you can reorder before running out."
}


# ----------------------------------------------------------
# Utility: Extract dishes (works with or without spaCy)
# ----------------------------------------------------------
DISH_KEYWORDS = [
    "pizza","burger","pasta","salad","soup","steak","fries","tacos","biryani",
    "sandwich","wrap","momos","noodles","ramen","curry","pancakes","omelette"
]

def extract_dish(text):
    """Extract dish name from text using spaCy if available, otherwise keyword matching"""
    text_lower = text.lower()
    
    # First try spaCy if available
    if NLP_AVAILABLE and nlp is not None:
        try:
            doc = nlp(text_lower)
            for np in doc.noun_chunks:
                for dish in DISH_KEYWORDS:
                    if dish in np.text:
                        return dish
        except:
            pass
    
    # Fallback to simple keyword matching
    for dish in DISH_KEYWORDS:
        if dish in text_lower:
            return dish
    
    return "Unknown"


# ----------------------------------------------------------
# Utility: LLM Summary Generator (OpenRouter)
# ----------------------------------------------------------
def generate_llm_summary(text):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You summarize restaurant reviews and extract insights."},
                {"role": "user", "content": f"Summarize the following reviews:\n\n{text}"}
            ]
        }

        res = requests.post(url, headers=headers, json=payload)
        data = res.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"LLM summary failed: {str(e)}"

# ----------------------------------------------------------
# Utility: Sales Forecasting with ARIMA
# ----------------------------------------------------------
def forecast_sales(sales_data, periods=7):
    """Forecast sales using ARIMA model (optional feature)"""
    if not HAS_STATSMODELS:
        return None
    
    try:
        if len(sales_data) < 4:
            return None
        
        # Ensure we have a proper array/series
        if isinstance(sales_data, np.ndarray):
            sales_array = sales_data
        else:
            sales_array = np.array(sales_data)
        
        model = ARIMA(sales_array, order=(1, 1, 1))
        fitted_model = model.fit()
        forecast = fitted_model.get_forecast(steps=periods)
        
        # Handle the forecast result - it may be Series or array
        forecast_values = forecast.predicted_mean
        if hasattr(forecast_values, 'values'):
            return forecast_values.values
        else:
            return np.array(forecast_values)
    except Exception as e:
        return None

# ----------------------------------------------------------
# Utility: Generate Dish Performance Ranking
# ----------------------------------------------------------
def get_dish_performance(df, pos_df):
    """Rank dishes by sentiment, sales, and popularity"""
    if df.empty or 'dish' not in df.columns:
        return pd.DataFrame()
    
    # Sentiment metrics
    sentiment_by_dish = df.groupby('dish').agg({
        'sentiment': ['mean', 'count'],
        'sentiment_label': lambda x: (x == 'Positive').sum()
    }).round(3)
    sentiment_by_dish.columns = ['avg_sentiment', 'review_count', 'positive_count']
    
    # Sales metrics
    if not pos_df.empty and 'item' in pos_df.columns and 'qty' in pos_df.columns:
        sales_by_dish = pos_df.groupby('item').agg({
            'qty': 'sum',
            'price': 'mean'
        }).round(2)
        sales_by_dish.columns = ['total_qty', 'avg_price']
        
        # Merge
        performance = sentiment_by_dish.join(sales_by_dish, how='outer').fillna(0)
    else:
        performance = sentiment_by_dish.copy()
        performance['total_qty'] = 0
        performance['avg_price'] = 0
    
    # Calculate performance score
    performance['sentiment_score'] = (performance['avg_sentiment'] + 1) / 2 * 100  # 0-100
    performance['popularity_score'] = (performance['review_count'] / performance['review_count'].max() * 100).fillna(0)
    performance['sales_score'] = (performance['total_qty'] / performance['total_qty'].max() * 100).fillna(0)
    performance['overall_score'] = (performance['sentiment_score'] * 0.4 + performance['popularity_score'] * 0.3 + performance['sales_score'] * 0.3).round(1)
    
    return performance.sort_values('overall_score', ascending=False)

# ----------------------------------------------------------
# Utility: Inventory Alerts
# ----------------------------------------------------------
def generate_inventory_alerts(inv_df, pos_df):
    """Generate inventory alerts based on stock levels and sales"""
    if inv_df.empty:
        return []
    
    alerts = []
    
    # Calculate average daily sales
    if not pos_df.empty and 'item' in pos_df.columns and 'qty' in pos_df.columns:
        daily_sales = pos_df.groupby('item')['qty'].sum()
    else:
        daily_sales = pd.Series()
    
    for _, row in inv_df.iterrows():
        item = row.get('item', 'Unknown')
        qty_on_hand = row.get('qty_on_hand', 0)
        
        avg_daily = daily_sales.get(item, 1)
        if avg_daily == 0:
            avg_daily = 1
        
        days_remaining = qty_on_hand / avg_daily if avg_daily > 0 else 999
        
        if days_remaining < 3:
            alerts.append({
                'item': item,
                'type': 'danger',
                'message': f"🚨 LOW STOCK: {item} has only {days_remaining:.1f} days of stock remaining",
                'qty': qty_on_hand
            })
        elif days_remaining < 7:
            alerts.append({
                'item': item,
                'type': 'warning',
                'message': f"⚠️ REORDER SOON: {item} will run out in {days_remaining:.1f} days",
                'qty': qty_on_hand
            })
        elif days_remaining > 30:
            alerts.append({
                'item': item,
                'type': 'info',
                'message': f"ℹ️ OVERSTOCK: {item} has {days_remaining:.0f} days of stock (consider promotion)",
                'qty': qty_on_hand
            })
    
    return alerts

# ----------------------------------------------------------
# Main Dashboard UI
# ----------------------------------------------------------
st.title("🍽️ Restaurant AI Dashboard")
st.markdown("*Real-time insights powered by AI — Local Compute + OpenRouter LLM*")

# ----------------------------------------------------------
# Load CSV files from data folder
# ----------------------------------------------------------
DATA_DIR = Path(__file__).parent / "data"

# Find available CSV files
available_files = {}
if DATA_DIR.exists():
    for csv_file in DATA_DIR.glob("*.csv"):
        available_files[csv_file.stem] = csv_file

if not available_files:
    st.error(f"❌ No CSV files found in {DATA_DIR} folder")
    st.stop()

# ----------------------------------------------------------
# Initialize data
# ----------------------------------------------------------
df = pd.DataFrame()
df_pos = pd.DataFrame()
df_inv = pd.DataFrame()
text_column = None

# Load Reviews
reviews_file = available_files.get("restaurant_reviews") or available_files.get("reviews") or available_files.get("mapped_reviews_export")
if reviews_file:
    try:
        df = pd.read_csv(reviews_file, on_bad_lines='skip', engine='python')
    except Exception as e:
        st.error(f"❌ Error reading reviews file: {e}")
        st.info("Please check your CSV file format")
        df = pd.DataFrame()

# Load POS
pos_file = available_files.get("pos_sales") or available_files.get("pos")
if pos_file:
    try:
        df_pos = pd.read_csv(pos_file)
    except Exception as e:
        st.warning(f"⚠️ Could not load POS data: {e}")
        df_pos = pd.DataFrame()

# Load Inventory
inv_file = available_files.get("inventory")
if inv_file:
    try:
        df_inv = pd.read_csv(inv_file)
    except Exception as e:
        st.warning(f"⚠️ Could not load inventory data: {e}")
        df_inv = pd.DataFrame()

# ----------------------------------------------------------
# Detect text column
# ----------------------------------------------------------
if not df.empty:
    possible_names = ['text', 'review_text', 'review', 'content', 'comment', 'message', 'description']
    for col in possible_names:
        if col in df.columns:
            text_column = col
            break
    
    # If still not found, use first string column
    if text_column is None:
        for col in df.columns:
            if df[col].dtype == 'object':
                text_column = col
                break

# ----------------------------------------------------------
# Process data (only if we have the text column)
# ----------------------------------------------------------
if not df.empty and text_column and text_column in df.columns:
    df["dish"] = df[text_column].apply(extract_dish)
    df["sentiment"] = df[text_column].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df["sentiment_label"] = df["sentiment"].apply(lambda x: "Positive" if x>0.1 else "Negative" if x<-0.1 else "Neutral")
elif not df.empty:
    # If no suitable text column, create default values
    df["dish"] = "Unknown"
    df["sentiment"] = 0
    df["sentiment_label"] = "Neutral"

# ----------------------------------------------------------
# Dashboard Tabs
# ----------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🏆 Dish Performance", "📦 Inventory", "📈 Forecasting", "🔍 Reviews"])

# ==================== TAB 1: OVERVIEW ====================
with tab1:
    st.subheader("📊 Dashboard Overview")
    st.markdown("""<div class="explanation">
    💡 This page gives you a quick snapshot of your restaurant's performance today. 
    See how many reviews you got, how satisfied your customers are, and which dishes are most popular.
    </div>""", unsafe_allow_html=True)
    
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Total Reviews", len(df), help="Total number of customer reviews received")
        with col2:
            avg_sentiment = df["sentiment"].mean() if "sentiment" in df.columns else 0
            sentiment_emoji = "😊" if avg_sentiment > 0.3 else "😐" if avg_sentiment > -0.3 else "😟"
            st.metric(f"{sentiment_emoji} Sentiment Score", f"{avg_sentiment:.2f}", 
                     help="How happy customers are (-1 = unhappy, +1 = very happy)")
        with col3:
            if "sentiment_label" in df.columns:
                positive_pct = (df["sentiment_label"] == "Positive").sum() / max(len(df), 1) * 100
            else:
                positive_pct = 0
            st.metric("😊 Happy Customers", f"{positive_pct:.0f}%", help="Percentage of positive reviews")
        with col4:
            if not df_pos.empty and 'qty' in df_pos.columns:
                total_sales = df_pos['qty'].sum()
                st.metric("📦 Items Sold", int(total_sales), help="Total items sold in the period")
            else:
                st.metric("📦 Items Sold", "N/A")
        
        st.divider()
        
        # Sentiment distribution chart
        col1, col2 = st.columns(2)
        with col1:
            if "sentiment_label" in df.columns:
                sentiment_counts = df["sentiment_label"].value_counts()
                fig = px.pie(sentiment_counts, values=sentiment_counts.values, names=sentiment_counts.index, 
                            title="How Customers Feel About Your Restaurant", hole=0.3,
                            color_discrete_map={"Positive": "#4caf50", "Negative": "#f44", "Neutral": "#9e9e9e"})
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(f"<div class='explanation'>{EXPLANATIONS['sentiment']}</div>", unsafe_allow_html=True)
        
        with col2:
            # Top dishes
            if "dish" in df.columns:
                top_dishes = df["dish"].value_counts().head(10)
                fig = px.bar(x=top_dishes.values, y=top_dishes.index, orientation='h',
                            title="Most Talked About Dishes", labels={"x": "Number of Reviews", "y": "Dish"},
                            color=top_dishes.values, color_continuous_scale='viridis')
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("<div class='explanation'>📊 Which dishes are customers talking about the most?</div>", unsafe_allow_html=True)
    else:
        st.warning("❌ No review data found. Please check your CSV files.")

# ==================== TAB 2: DISH PERFORMANCE ====================
with tab2:
    st.subheader("🏆 Which Dishes Are Your Stars?")
    st.markdown("""<div class="explanation">
    💡 This page shows you which dishes customers love the most and which ones might need improvement.
    Score = (Happiness × 40%) + (Popularity × 30%) + (Sales × 30%)
    </div>""", unsafe_allow_html=True)
    
    if not df.empty:
        performance = get_dish_performance(df, df_pos)
        
        if not performance.empty:
            # Ranking table with plain language
            ranking_df = performance[['avg_sentiment', 'review_count', 'positive_count', 'total_qty', 'overall_score']].copy()
            ranking_df.columns = ['😊 Happiness', '📝 Reviews', '👍 Positive', '📦 Sold', '⭐ Score']
            ranking_df = ranking_df.round(1)
            
            st.dataframe(ranking_df, use_container_width=True, height=400)
            
            st.markdown("""
            **How to read this table:**
            - 😊 Happiness: Average customer satisfaction (-1 to +1, higher is better)
            - 📝 Reviews: How many times this dish was mentioned
            - 👍 Positive: How many positive reviews it got
            - 📦 Sold: How many of this dish you sold
            - ⭐ Score: Overall performance (0-100, higher is better)
            """)
            
            st.divider()
            
            # Performance chart
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(performance.reset_index(), x='overall_score', y=performance.index, 
                           orientation='h', title="⭐ Dish Performance Scores",
                           labels={"overall_score": "Performance Score (0-100)", "dish": "Dish"},
                           color='overall_score', color_continuous_scale='RdYlGn',
                           text='overall_score')
                fig.update_traces(textposition='auto')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("<div class='explanation'>🟢 Green = Great! 🟡 Yellow = OK 🔴 Red = Needs work</div>", unsafe_allow_html=True)
            
            with col2:
                fig = px.scatter(performance.reset_index(), x='avg_sentiment', y='total_qty', size='review_count',
                               title="💰 Happiness vs Sales", hover_data=['review_count'],
                               labels={"avg_sentiment": "Customer Satisfaction", "total_qty": "Items Sold", "review_count": "Reviews"},
                               color='overall_score', color_continuous_scale='viridis')
                fig.add_hline(y=0)
                fig.add_vline(x=0)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("<div class='explanation'>📈 Top right = Happy customers + High sales = Star dish!</div>", unsafe_allow_html=True)
        else:
            st.info("ℹ️ Not enough data for performance analysis yet. Check back after more reviews!")
    else:
        st.warning("❌ No review data available")

# ==================== TAB 3: INVENTORY ====================
with tab3:
    st.subheader("📦 Check Your Stock Levels")
    st.markdown("""<div class="explanation">
    💡 Keep an eye on your inventory! This page warns you before items run out so you can reorder in time.
    Days Remaining = Current Stock ÷ Average Daily Sales
    </div>""", unsafe_allow_html=True)
    
    if not df_inv.empty:
        # Generate alerts
        alerts = generate_inventory_alerts(df_inv, df_pos)
        
        if alerts:
            st.subheader("⚠️ Stock Alerts")
            for alert in alerts:
                if alert['type'] == 'danger':
                    st.markdown(f"""<div class="alert-danger"><strong>🚨 CRITICAL:</strong> {alert['message']}</div>""", unsafe_allow_html=True)
                elif alert['type'] == 'warning':
                    st.markdown(f"""<div class="alert-warning"><strong>⚠️ WARNING:</strong> {alert['message']}</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="alert-success"><strong>ℹ️ INFO:</strong> {alert['message']}</div>""", unsafe_allow_html=True)
            st.divider()
        else:
            st.success("✅ All items have healthy stock levels!")
        
        # Inventory table with better column names
        st.subheader("Current Stock Levels")
        st.dataframe(df_inv, use_container_width=True, hide_index=True)
        
        # Stock visualization
        if 'qty_on_hand' in df_inv.columns and 'item' in df_inv.columns:
            fig = px.bar(df_inv.sort_values('qty_on_hand', ascending=True), 
                        x='qty_on_hand', y='item', orientation='h',
                        title="📊 Stock Levels (Green = Good, Red = Low)",
                        labels={"qty_on_hand": "Quantity in Stock", "item": "Item"},
                        color='qty_on_hand', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ No inventory data loaded. Upload inventory.csv to see stock alerts.")

# ==================== TAB 4: FORECASTING ====================
with tab4:
    st.subheader("📈 Predict Your Sales")
    st.markdown("""<div class="explanation">
    💡 This predicts what you'll sell in the next 2 weeks based on your recent sales patterns.
    Use this to plan staffing, ordering, and promotions!
    </div>""", unsafe_allow_html=True)
    
    if not HAS_STATSMODELS:
        st.warning("⚠️ Forecasting feature needs statsmodels. Install with: `pip install statsmodels`")
        st.info("Other features are working fine. This is an optional advanced feature.")
    elif not df_pos.empty and 'date' in df_pos.columns and 'qty' in df_pos.columns:
        try:
            # Prepare time series data
            df_pos_copy = df_pos.copy()
            df_pos_copy['date'] = pd.to_datetime(df_pos_copy['date'], errors='coerce')
            daily_sales = df_pos_copy.groupby('date')['qty'].sum().sort_index()
            
            if len(daily_sales) > 4:
                # Forecast
                forecast_values = forecast_sales(daily_sales.values, periods=14)
                
                if forecast_values is not None and len(forecast_values) > 0:
                    # Create forecast dataframe
                    last_date = daily_sales.index[-1]
                    future_dates = [last_date + timedelta(days=i+1) for i in range(len(forecast_values))]
                    forecast_df = pd.DataFrame({
                        'date': future_dates,
                        'forecast': forecast_values
                    })
                    
                    # Plot
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=daily_sales.index, y=daily_sales.values, 
                                           mode='lines', name='Your Past Sales', 
                                           line=dict(color='blue', width=3)))
                    fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['forecast'],
                                           mode='lines+markers', name='Predicted Sales',
                                           line=dict(color='orange', width=3, dash='dash')))
                    fig.update_layout(title="📊 Sales Forecast (Next 14 Days)", 
                                    xaxis_title="Date", yaxis_title="Items to Sell", 
                                    height=400, hovermode='x unified')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📊 Your Avg Daily Sales", f"{daily_sales.mean():.0f} items", 
                                 help="How many items you sold per day on average")
                    with col2:
                        st.metric("🔮 Predicted Avg Daily", f"{forecast_df['forecast'].mean():.0f} items",
                                 help="What we predict you'll sell per day")
                    with col3:
                        trend = "📈 Going UP" if forecast_df['forecast'].mean() > daily_sales.mean() else "📉 Going DOWN" if forecast_df['forecast'].mean() < daily_sales.mean() else "➡️ STABLE"
                        change = int((forecast_df['forecast'].mean() - daily_sales.mean()) / max(daily_sales.mean(), 1) * 100)
                        st.metric("📈 Trend", f"{change:+d}%", help="How much your sales are expected to change")
                    
                    st.markdown("""
                    **💡 What to do with this forecast:**
                    - 📦 Plan your inventory orders based on predicted sales
                    - 👥 Schedule enough staff for busy days
                    - 📢 Run promotions if you predict a slow period
                    - 💰 Prepare financially for higher/lower revenue
                    """)
                else:
                    st.warning("❌ Couldn't generate forecast. Try again later when you have more data.")
            else:
                st.info("📊 Need at least 5 days of sales data to predict. Check back soon!")
        except Exception as e:
            st.error(f"❌ Forecasting error: {str(e)}")
    else:
        st.info("ℹ️ Forecasting needs sales data with 'date' and 'qty' columns. Check your POS file.")

# ==================== TAB 5: REVIEWS ====================
with tab5:
    st.subheader("🔍 Read Customer Reviews")
    st.markdown("""<div class="explanation">
    💡 See what customers are saying about your restaurant. Look for patterns to understand what's working
    and what needs improvement.
    </div>""", unsafe_allow_html=True)
    
    if not df.empty and text_column:
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Total Reviews", len(df))
        with col2:
            if "sentiment_label" in df.columns:
                avg_rating = (df["sentiment"] * 5).mean()  # Convert to 5-star scale
                st.metric("⭐ Average Rating", f"{avg_rating:.1f} / 5")
        with col3:
            if "rating" in df.columns and not df["rating"].empty:
                st.metric("🎯 Customer Rating", f"{df['rating'].mean():.1f} / 5")
        
        st.divider()
        
        # Show reviews
        st.subheader("Recent Reviews")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            if "sentiment_label" in df.columns:
                sentiment_filter = st.selectbox("Filter by sentiment:", 
                                               ["All", "Positive 😊", "Negative 😟", "Neutral 😐"],
                                               help="Show only reviews of a certain type")
        with col2:
            review_limit = st.slider("Show last N reviews:", 5, 100, 20)
        
        # Apply filters
        filtered_df = df.copy()
        if sentiment_filter == "Positive 😊" and "sentiment_label" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["sentiment_label"] == "Positive"]
        elif sentiment_filter == "Negative 😟" and "sentiment_label" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["sentiment_label"] == "Negative"]
        elif sentiment_filter == "Neutral 😐" and "sentiment_label" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["sentiment_label"] == "Neutral"]
        
        # Show reviews in a nice format
        for idx, (_, row) in enumerate(filtered_df.tail(review_limit).iterrows()):
            sentiment = row.get("sentiment_label", "Neutral")
            emoji = "😊" if sentiment == "Positive" else "😟" if sentiment == "Negative" else "😐"
            rating = row.get("rating", "")
            date = row.get("date", "")
            
            review_text = row.get(text_column, "")
            
            st.markdown(f"""
            <div style="background-color:#f5f5f5; padding:1rem; margin:0.5rem 0; border-radius:5px; border-left: 4px solid #2196F3;">
            <strong>{emoji} {sentiment}</strong> {f"| ⭐ {rating}" if rating else ""} {f"| {date}" if date else ""}
            <br/>
            {review_text}
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # LLM Summary
        st.subheader("🤖 AI-Powered Summary")
        if st.button("📊 Generate AI Insights About Your Reviews", use_container_width=True):
            with st.spinner("🤔 AI is analyzing your reviews..."):
                reviews_sample = "\n".join(filtered_df[text_column].astype(str).head(50).tolist())
                summary = generate_llm_summary(reviews_sample)
                st.markdown(summary)
                st.success("✅ Summary complete!")
    else:
        st.warning("❌ No review data available. Check your CSV files.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set dashboard configuration
st.set_page_config(page_title="Veridi Logistics Auditor", layout="wide", page_icon="🚚")

# --- Title and Hero ---
st.title("🚚 Veridi Logistics: Last Mile Auditor")
st.markdown("""
### Delivery Performance & Customer Sentiment Analysis
An interactive dashboard to identify regional logistics bottlenecks and prioritize infrastructure improvements for the highest business ROI.
""")

# --- Data Loading and Caching ---
@st.cache_data
def load_and_clean_data():
    # 1. Load datasets
    orders = pd.read_csv('olist_orders_dataset.csv')
    reviews = pd.read_csv('olist_order_reviews_dataset.csv')
    customers = pd.read_csv('olist_customers_dataset.csv')
    products = pd.read_csv('olist_products_dataset.csv')
    translation = pd.read_csv('product_category_name_translation.csv')

    # 2. Join Pipeline
    # Deduplicate reviews (latest per order)
    reviews_clean = reviews.sort_values('review_answer_timestamp', ascending=False).drop_duplicates('order_id')
    
    # Master Merge
    df = orders.merge(customers, on='customer_id', how='left')
    df = df.merge(reviews_clean, on='order_id', how='left')
    
    # 3. Delay Logistics
    # Filter for intended deliveries
    df = df[~df['order_status'].isin(['canceled', 'unavailable'])]
    df = df.dropna(subset=['order_delivered_customer_date'])
    
    # Date Conversion
    date_cols = ['order_estimated_delivery_date', 'order_delivered_customer_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    
    # Days_Difference = Estimated - Actual (Positive = On Time, Negative = Late)
    df['Days_Difference'] = (df['order_estimated_delivery_date'] - df['order_delivered_customer_date']).dt.days
    
    # Classification
    def classify_delivery(diff):
        if diff >= 0: return 'On Time'
        elif diff >= -5: return 'Late'
        else: return 'Super Late'
    df['Delivery_Status'] = df['Days_Difference'].apply(classify_delivery)
    df['Is_Late'] = df['Delivery_Status'].isin(['Late', 'Super Late'])
    df['Days_Late_Abs'] = np.where(df['Days_Difference'] < 0, abs(df['Days_Difference']), 0)
    
    # 4. Products Bridge (Physical Attributes)
    # Join products for shipping difficulty analysis
    prod_trans = products.merge(translation, on='product_category_name', how='left')
    prod_trans['category_en'] = prod_trans['product_category_name_english'].fillna(prod_trans['product_category_name'])
    
    # Calculate Volume
    prod_trans['volume_cm3'] = prod_trans['product_length_cm'] * prod_trans['product_height_cm'] * prod_trans['product_width_cm']
    
    return df, prod_trans

# Load Data
with st.spinner("Loading Veridi Logistics Data... (100k+ rows)"):
    full_df, product_df = load_and_clean_data()

# --- Sidebar Filters ---
st.sidebar.header("📋 Audit Controls")
selected_states = st.sidebar.multiselect("Select State(s) to Audit", 
                                       options=sorted(full_df['customer_state'].unique()), 
                                       default=None)

# Apply Filters
df = full_df.copy()
if selected_states:
    df = df[df['customer_state'].isin(selected_states)]

# --- Main KPI Scoreboard ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

late_pct = (df['Is_Late'].mean() * 100)
avg_score = df['review_score'].mean()

kpi1.metric("📦 Total Orders Audit", f"{len(df):,}")
kpi2.metric("❌ Overall Delay Rate", f"{late_pct:.1f}%", delta=f"{late_pct-10:.1f}%", delta_color="inverse")
kpi3.metric("⭐ Avg Review Score", f"{avg_score:.2f}")
kpi4.metric("📈 Business Hubs", len(df['customer_state'].unique()))

st.divider()

# --- Dashboard Layout (Tabs) ---
tab_audit, tab_sentiment, tab_strategy = st.tabs(["📊 Regional Audit", "❤️ Sentiment Discovery", "🎯 Strategic Fix (ROI)"])

with tab_audit:
    col_a1, col_a2 = st.columns([1, 1])
    
    with col_a1:
        st.subheader("State-Level Failure Rates")
        state_stats = full_df.groupby('customer_state').agg(
            Late_Pct=('Is_Late', 'mean'),
            Total_Orders=('order_id', 'count')
        ).reset_index()
        state_stats['Late_Pct'] *= 100
        state_stats_sorted = state_stats.sort_values('Late_Pct', ascending=False)
        
        fig_states = px.bar(state_stats_sorted, x='Late_Pct', y='customer_state', orientation='h',
                           title="Percent of Late Deliveries by State",
                           labels={'Late_Pct': '% Delayed', 'customer_state': 'State Code'},
                           color='Late_Pct', color_continuous_scale='Reds')
        st.plotly_chart(fig_states, use_container_width=True)

    with col_a2:
        st.subheader("What do 'Late' Deliveries look like?")
        status_dist = df['Delivery_Status'].value_counts().reset_index()
        fig_pie = px.pie(status_dist, values='count', names='Delivery_Status', 
                        hole=0.4, color='Delivery_Status',
                        color_discrete_map={'On Time': 'green', 'Late': 'orange', 'Super Late': 'red'})
        st.plotly_chart(fig_pie, use_container_width=True)

with tab_sentiment:
    st.subheader("The Cost of a Single Day Promptness")
    
    # Trend Analysis
    trend_df = df[df['Days_Late_Abs'] <= 30].groupby('Days_Late_Abs')['review_score'].mean().reset_index()
    fig_trend = px.line(trend_df, x='Days_Late_Abs', y='review_score', markers=True,
                       title="Review Score degradation vs. Days Delayed",
                       labels={'Days_Late_Abs': 'Days Delivered Late', 'review_score': 'Avg Score (1-5)'})
    fig_trend.update_traces(line_color='red')
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.info("**Logistics Insight:** Customer sentiment drops sharply under a 2.5 score as soon as the delay exceeds 5 days.")

with tab_strategy:
    st.subheader("Business Impact Priority Score")
    st.markdown("We weight the **failure rate** by the **business volume share** of each state to find the most critical fixes.")
    
    total_national = state_stats['Total_Orders'].sum()
    state_stats['Volume_Share'] = (state_stats['Total_Orders'] / total_national) * 100
    state_stats['Priority_Score'] = state_stats['Volume_Share'] * state_stats['Late_Pct']
    
    fig_strategy = px.scatter(state_stats, x='Late_Pct', y='Volume_Share', size='Priority_Score',
                             color='Priority_Score', hover_name='customer_state',
                             title="Logistics ROI Prioritization (Volume vs. Delay)",
                             labels={'Late_Pct': 'Failure Rate (%)', 'Volume_Share': 'Business Share (%)'},
                             color_continuous_scale='Reds', size_max=40)
    
    # Add quadrant lines
    fig_strategy.add_hline(y=state_stats['Volume_Share'].mean(), line_dash="dot", line_color="green", annotation_text="Avg Volume")
    fig_strategy.add_vline(x=state_stats['Late_Pct'].mean(), line_dash="dot", line_color="blue", annotation_text="Avg Failure")
    
    st.plotly_chart(fig_strategy, use_container_width=True)
    
    # Compare Furniture vs Electronics attributes
    st.divider()
    st.subheader("The Category Challenge: Why is Furniture Harder?")
    
    target_cats = ['furniture_decor', 'electronics', 'computers', 'telephony', 'computers_accessories']
    comp_cats = product_df[product_df['category_en'].isin(target_cats)].groupby('category_en')[['product_weight_g', 'volume_cm3']].mean().reset_index()
    comp_cats['weight_kg'] = comp_cats['product_weight_g'] / 1000

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.plotly_chart(px.bar(comp_cats.sort_values('weight_kg'), x='weight_kg', y='category_en', title="Avg Weight (kg)"), use_container_width=True)
    with col_c2:
        st.plotly_chart(px.bar(comp_cats.sort_values('volume_cm3'), x='volume_cm3', y='category_en', title="Avg Volume (cm³)"), use_container_width=True)

# --- Footer ---
st.divider()
st.caption("Veridi Logistics - Data Audit Tool v1.0 | Created by NSS Capstone Senior Analyst")

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Disbursement Projection Calculator",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for colorful styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(120deg, #ffd700, #ffed4e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #e0e7ff;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    .success-alert {
        padding: 1.5rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 1rem;
        margin-top: 1.5rem;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
    }
    
    .error-alert {
        padding: 1.5rem;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 1rem;
        margin-top: 1.5rem;
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
    }
    
    .info-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }
    
    .performance-card {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
        margin-bottom: 1rem;
    }
    
    .performance-card h3 {
        color: #fbbf24;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .performance-card ul {
        list-style: none;
        padding: 0;
    }
    
    .performance-card li {
        padding: 0.5rem 0;
        font-size: 1.1rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .performance-card li:last-child {
        border-bottom: none;
    }
    
    .stDataFrame {
        background: white;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    h3 {
        color: #fbbf24 !important;
        font-weight: 700;
        font-size: 1.8rem;
        margin-top: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .stSelectbox, .stNumberInput {
        background: white;
        border-radius: 0.8rem;
    }
    
    div[data-baseweb="select"] {
        background: white;
        border-radius: 0.8rem;
    }
    
    .input-label {
        color: white !important;
        font-weight: 600;
        font-size: 1.1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .metric-card-blue {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
    }
    
    .metric-card-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.4);
    }
    
    .metric-card-amber {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
    }
    
    .table-container {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Disbursement pattern constants
DISBURSEMENT_PATTERN = {
    "Days 1-5": 21.27,
    "Days 6-10": 10.72,
    "Days 11-15": 7.77,
    "Days 16-20": 8.38,
    "Days 21-25": 12.45,
    "Days 26-31": 39.30
}

ALLOWED_DAYS = [0, 5, 10, 15, 20, 25, 31]

def get_cumulative_percentage_up_to_day(day):
    """Calculate cumulative expected percentage up to a given day"""
    cumulative = 0
    if day >= 1:
        cumulative += DISBURSEMENT_PATTERN["Days 1-5"]
    if day >= 6:
        cumulative += DISBURSEMENT_PATTERN["Days 6-10"]
    if day >= 11:
        cumulative += DISBURSEMENT_PATTERN["Days 11-15"]
    if day >= 16:
        cumulative += DISBURSEMENT_PATTERN["Days 16-20"]
    if day >= 21:
        cumulative += DISBURSEMENT_PATTERN["Days 21-25"]
    if day >= 26:
        cumulative += DISBURSEMENT_PATTERN["Days 26-31"]
    return min(cumulative, 100)

def calculate_projections(days_passed, target_amount, amount_disbursed):
    """Calculate all projections and metrics"""
    days = max(0, min(31, days_passed))
    target = max(0.1, target_amount)
    disbursed = max(0, amount_disbursed)
    
    # Calculate expected percentage and amount
    cumulative_expected_percentage = get_cumulative_percentage_up_to_day(days)
    expected_amount = (target * cumulative_expected_percentage) / 100
    
    # Calculate actual percentage
    actual_percentage = (disbursed / target) * 100
    
    # Calculate implied total
    if cumulative_expected_percentage > 0 and disbursed > 0:
        implied_total = disbursed / (cumulative_expected_percentage / 100)
    else:
        implied_total = target
    
    # Calculate projections for remaining periods
    projection_data = []
    total_projected = disbursed
    total_historical_remaining_pct = 0
    
    # Find remaining periods
    remaining_periods = []
    for period, percentage in DISBURSEMENT_PATTERN.items():
        period_start = int(period.split("-")[0].replace("Days ", ""))
        if period_start > days:
            remaining_periods.append({"period": period, "percentage": percentage})
            total_historical_remaining_pct += percentage
    
    # Calculate projections
    for item in remaining_periods:
        projected_amount = (implied_total * item["percentage"]) / 100
        projection_data.append({
            "Period": item["period"],
            "Historical %": item["percentage"],
            "At Current Pace (CR)": projected_amount,
            "To Hit Target (CR)": projected_amount  # Will be adjusted below
        })
        total_projected += projected_amount
    
    # Adjust amounts to hit target
    remaining_target = target - disbursed
    if remaining_periods and total_historical_remaining_pct > 0:
        for item in projection_data:
            proportion_of_remaining = item["Historical %"] / total_historical_remaining_pct
            item["To Hit Target (CR)"] = remaining_target * proportion_of_remaining
    
    gap = target - total_projected
    
    return {
        "cumulative_expected_percentage": cumulative_expected_percentage,
        "expected_amount": expected_amount,
        "actual_percentage": actual_percentage,
        "implied_total": implied_total,
        "total_projected": total_projected,
        "gap": gap,
        "projection_data": projection_data,
        "remaining_amount": target - disbursed,
        "remaining_days": 31 - days
    }

# Header
st.markdown('<div class="main-header">🎯 Disbursement Projection Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">✨ Monitor and optimize your monthly disbursement targets with style ✨</div>', unsafe_allow_html=True)

# Input section in colorful box
st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.markdown("### 📊 Input Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    days_passed = st.selectbox("📅 Days Passed", ALLOWED_DAYS, index=1)

with col2:
    target_amount = st.number_input("🎯 Target Amount (CR)", min_value=0.1, value=10.0, step=0.1, format="%.2f")

with col3:
    amount_disbursed = st.number_input("💰 Disbursed Till Now (CR)", min_value=0.0, value=1.0, step=0.1, format="%.2f")
st.markdown('</div>', unsafe_allow_html=True)

# Calculate results
results = calculate_projections(days_passed, target_amount, amount_disbursed)

# Display metrics in colorful cards
st.markdown("### 🌟 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card-blue">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: white; margin: 0;'>Target</h4>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: #fbbf24; margin: 0.5rem 0;'>₹{target_amount:.2f} CR</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    on_track = results["gap"] <= 0
    card_class = "metric-card-green" if on_track else "metric-card-red"
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: white; margin: 0;'>On Track?</h4>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: #fbbf24; margin: 0.5rem 0;'>{'✅ Yes' if on_track else '⚠️ No'}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: white; margin: 0;'>Gap: ₹{abs(results['gap']):.2f} CR</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card-green">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: white; margin: 0;'>Disbursed So Far</h4>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: #fbbf24; margin: 0.5rem 0;'>₹{amount_disbursed:.2f} CR</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: white; margin: 0;'>{results['actual_percentage']:.2f}%</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card-amber">', unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: white; margin: 0;'>Expected by Day {days_passed}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: #fbbf24; margin: 0.5rem 0;'>₹{results['expected_amount']:.2f} CR</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: white; margin: 0;'>{results['cumulative_expected_percentage']:.2f}%</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Projection table
st.markdown("### 📈 Disbursement Projection for Upcoming Periods")

if results["projection_data"]:
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    df = pd.DataFrame(results["projection_data"])
    
    # Format the dataframe
    df["Historical %"] = df["Historical %"].apply(lambda x: f"{x:.2f}%")
    df["At Current Pace (CR)"] = df["At Current Pace (CR)"].apply(lambda x: f"₹{x:.3f}")
    df["To Hit Target (CR)"] = df["To Hit Target (CR)"].apply(lambda x: f"₹{x:.3f}")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🎉 No upcoming periods to display - you've reached the end of the month!")

# Performance cards
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="performance-card">', unsafe_allow_html=True)
    st.markdown("<h3>📊 Current Performance</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <ul>
        <li><strong>Implied Total:</strong> ₹{results['implied_total']:.2f} CR</li>
        <li><strong>Actual %:</strong> {results['actual_percentage']:.2f}%</li>
        <li><strong>Expected %:</strong> {results['cumulative_expected_percentage']:.2f}%</li>
        <li><strong>If continuing at current pace:</strong> ₹{results['total_projected']:.2f} CR</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="performance-card">', unsafe_allow_html=True)
    st.markdown("<h3>🎯 To Achieve Target</h3>", unsafe_allow_html=True)
    daily_avg = results['remaining_amount'] / max(1, results['remaining_days'])
    st.markdown(f"""
    <ul>
        <li><strong>Remaining Amount:</strong> ₹{results['remaining_amount']:.2f} CR</li>
        <li><strong>Remaining Days:</strong> {results['remaining_days']} days</li>
        <li><strong>Required daily average:</strong> ₹{daily_avg:.3f} CR/day</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Alert message
if results["gap"] > 0:
    st.markdown(f"""
    <div class="error-alert">
        <h3 style="color: #fbbf24; margin-top: 0;">⚠️ Alert: On Track to Miss Target</h3>
        <p style="font-size: 1.1rem;">You are on track to disburse only <strong>₹{results['total_projected']:.2f} CR</strong>, 
        short by <strong>₹{results['gap']:.2f} CR</strong>.</p>
        <p style="font-size: 1.1rem;">You need to increase disbursement in upcoming periods to meet the target. 
        The "To Hit Target" column shows what you should disburse in each period to achieve ₹{target_amount:.2f} CR.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="success-alert">
        <h3 style="color: #fbbf24; margin-top: 0;">✅ On Track: Target Achievement Confirmed</h3>
        <p style="font-size: 1.1rem;">At your current pace, you will exceed the target and potentially disburse 
        <strong>₹{results['total_projected']:.2f} CR</strong>.</p>
        <p style="font-size: 1.1rem;">Great work! Continue maintaining this momentum. 🚀</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: white; font-size: 1.1rem;'>Built with ❤️ using Streamlit | Disbursement Projection Calculator</div>", unsafe_allow_html=True)

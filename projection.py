import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Disbursement Projection Calculator",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .metric-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-alert {
        padding: 1rem;
        background-color: #dcfce7;
        border-left: 4px solid #22c55e;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .error-alert {
        padding: 1rem;
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        border-radius: 0.5rem;
        margin-top: 1rem;
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
st.markdown('<div class="sub-header">Monitor and optimize your monthly disbursement targets</div>', unsafe_allow_html=True)

# Input section
st.markdown("### Input Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    days_passed = st.selectbox("Days Passed", ALLOWED_DAYS, index=1)

with col2:
    target_amount = st.number_input("Target Amount (CR)", min_value=0.1, value=10.0, step=0.1, format="%.2f")

with col3:
    amount_disbursed = st.number_input("Disbursed Till Now (CR)", min_value=0.0, value=1.0, step=0.1, format="%.2f")

# Calculate results
results = calculate_projections(days_passed, target_amount, amount_disbursed)

# Display metrics
st.markdown("---")
st.markdown("### Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Target",
        value=f"₹{target_amount:.2f} CR",
        delta=None
    )

with col2:
    on_track = "Yes" if results["gap"] <= 0 else "No"
    st.metric(
        label="On Track?",
        value=on_track,
        delta=f"Gap: ₹{abs(results['gap']):.2f} CR",
        delta_color="normal" if results["gap"] <= 0 else "inverse"
    )

with col3:
    st.metric(
        label="Disbursed So Far",
        value=f"₹{amount_disbursed:.2f} CR",
        delta=f"{results['actual_percentage']:.2f}%"
    )

with col4:
    st.metric(
        label=f"Expected by Day {days_passed}",
        value=f"₹{results['expected_amount']:.2f} CR",
        delta=f"{results['cumulative_expected_percentage']:.2f}%"
    )

# Projection table
st.markdown("---")
st.markdown("### 📊 Disbursement Projection for Upcoming Periods")

if results["projection_data"]:
    df = pd.DataFrame(results["projection_data"])
    
    # Format the dataframe
    df["Historical %"] = df["Historical %"].apply(lambda x: f"{x:.2f}%")
    df["At Current Pace (CR)"] = df["At Current Pace (CR)"].apply(lambda x: f"₹{x:.3f}")
    df["To Hit Target (CR)"] = df["To Hit Target (CR)"].apply(lambda x: f"₹{x:.3f}")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No upcoming periods to display.")

# Performance cards
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Current Performance")
    st.markdown(f"""
    - **Implied Total:** ₹{results['implied_total']:.2f} CR
    - **Actual %:** {results['actual_percentage']:.2f}%
    - **Expected %:** {results['cumulative_expected_percentage']:.2f}%
    - **If continuing at current pace:** ₹{results['total_projected']:.2f} CR
    """)

with col2:
    st.markdown("### 🎯 To Achieve Target")
    daily_avg = results['remaining_amount'] / max(1, results['remaining_days'])
    st.markdown(f"""
    - **Remaining Amount:** ₹{results['remaining_amount']:.2f} CR
    - **Remaining Days:** {results['remaining_days']} days
    - **Required daily average:** ₹{daily_avg:.3f} CR/day
    """)

# Alert message
st.markdown("---")
if results["gap"] > 0:
    st.markdown(f"""
    <div class="error-alert">
        <h3>⚠️ Alert: On Track to Miss Target</h3>
        <p>You are on track to disburse only <strong>₹{results['total_projected']:.2f} CR</strong>, 
        short by <strong>₹{results['gap']:.2f} CR</strong>.</p>
        <p>You need to increase disbursement in upcoming periods to meet the target. 
        The "To Hit Target" column shows what you should disburse in each period to achieve ₹{target_amount:.2f} CR.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="success-alert">
        <h3>✅ On Track: Target Achievement Confirmed</h3>
        <p>At your current pace, you will exceed the target and potentially disburse 
        <strong>₹{results['total_projected']:.2f} CR</strong>.</p>
        <p>Great work! Continue maintaining this momentum.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Disbursement Projection Calculator")

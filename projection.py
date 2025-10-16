import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Disbursement Projection Calculator",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS matching the design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0f172a;
    }
    
    .main {
        background-color: #0f172a;
        padding: 2rem;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Input section styling */
    .input-section {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem 2rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid #475569;
    }
    
    .input-section h3 {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
        margin-top: 0;
    }
    
    label {
        color: #e2e8f0 !important;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Metric cards - all same height */
    .metric-card-blue {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1.5rem;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card-red {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1.5rem;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1.5rem;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card-orange {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1.5rem;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
    }
    
    .metric-sub {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Table section */
    .table-section {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 0;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid #475569;
        overflow: hidden;
    }
    
    .table-header {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        color: #10b981;
        font-size: 1.3rem;
        font-weight: 600;
        padding: 1.2rem 1.5rem;
        margin: 0;
        display: flex;
        align-items: center;
        border-bottom: 2px solid #10b981;
    }
    
    .table-content {
        padding: 1.5rem;
    }
    
    /* Performance cards */
    .performance-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .performance-card h3 {
        color: #60a5fa;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    .perf-row {
        display: flex;
        justify-content: space-between;
        padding: 1rem 0;
        border-bottom: 1px solid #334155;
    }
    
    .perf-row:last-child {
        border-bottom: none;
    }
    
    .perf-label {
        color: #94a3b8;
        font-size: 1rem;
    }
    
    .perf-value {
        color: #60a5fa;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .perf-value-yellow {
        color: #fbbf24;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .perf-value-green {
        color: #10b981;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .perf-value-white {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .perf-big-value {
        color: #60a5fa;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    .perf-big-value-green {
        color: #10b981;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    /* Alert boxes */
    .alert-error {
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
        border-left: 4px solid #dc2626;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-top: 1.5rem;
        color: #fecaca;
    }
    
    .alert-error h3 {
        color: #fca5a5;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-top: 1.5rem;
        color: #a7f3d0;
    }
    
    .alert-success h3 {
        color: #6ee7b7;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: transparent !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: transparent !important;
    }
    
    /* Custom table styling */
    .dataframe {
        width: 100% !important;
        background-color: transparent !important;
    }
    
    .dataframe thead tr th {
        background-color: #1e293b !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 14px 12px !important;
        font-size: 0.95rem !important;
        border-bottom: 1px solid #475569 !important;
    }
    
    .dataframe tbody tr td {
        padding: 14px 12px !important;
        text-align: center !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        background-color: #1e293b !important;
        border-bottom: 1px solid #334155 !important;
    }
    
    .dataframe tbody tr:hover td {
        background-color: #334155 !important;
    }
    
    .dataframe tbody tr:last-child td {
        border-bottom: none !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input field styling */
    .stSelectbox > div > div {
        background-color: #475569 !important;
        border-color: #64748b !important;
        color: #ffffff !important;
    }
    
    .stNumberInput > div > div > input {
        background-color: #475569 !important;
        border-color: #64748b !important;
        color: #ffffff !important;
    }
    
    /* Hide empty container */
    .element-container:has(> .stMarkdown > div[data-testid="stMarkdownContainer"]:empty) {
        display: none;
    }
    
    /* Remove spacing between sections */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Fix column width consistency */
    div[data-testid="column"]:first-child {
        flex: 1 1 50% !important;
    }
    
    div[data-testid="column"]:last-child {
        flex: 1 1 50% !important;
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
    
    cumulative_expected_percentage = get_cumulative_percentage_up_to_day(days)
    expected_amount = (target * cumulative_expected_percentage) / 100
    actual_percentage = (disbursed / target) * 100
    
    if cumulative_expected_percentage > 0 and disbursed > 0:
        implied_total = disbursed / (cumulative_expected_percentage / 100)
    else:
        implied_total = target
    
    projection_data = []
    total_projected = disbursed
    total_historical_remaining_pct = 0
    
    remaining_periods = []
    for period, percentage in DISBURSEMENT_PATTERN.items():
        period_start = int(period.split("-")[0].replace("Days ", ""))
        if period_start > days:
            remaining_periods.append({"period": period, "percentage": percentage})
            total_historical_remaining_pct += percentage
    
    for item in remaining_periods:
        projected_amount = (implied_total * item["percentage"]) / 100
        projection_data.append({
            "Period": item["period"],
            "Historical %": item["percentage"],
            "At Current Pace (CR)": projected_amount,
            "To Hit Target (CR)": projected_amount
        })
        total_projected += projected_amount
    
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

# Input section
st.markdown('<div class="input-section"><h3>Input Parameters</h3>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    days_passed = st.selectbox("Days Passed", ALLOWED_DAYS, index=1)

with col2:
    target_amount = st.number_input("Target Amount (CR)", min_value=0.1, value=10.0, step=0.1, format="%.2f")

with col3:
    amount_disbursed = st.number_input("Disbursed Till Now (CR)", min_value=0.0, value=1.0, step=0.1, format="%.2f")

st.markdown('</div>', unsafe_allow_html=True)

# Calculate results
results = calculate_projections(days_passed, target_amount, amount_disbursed)

# Display metrics
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="metric-card-blue">
        <div class="metric-label">Target</div>
        <div class="metric-value">₹{target_amount:.2f} CR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card-green">
        <div class="metric-label">Disbursed So Far</div>
        <div class="metric-value">₹{amount_disbursed:.2f} CR</div>
        <div class="metric-sub">{results['actual_percentage']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    on_track = results["gap"] <= 0
    card_class = "metric-card-green" if on_track else "metric-card-red"
    status_text = "Yes" if on_track else "No"
    icon = "✓" if on_track else "⚠"
    
    st.markdown(f"""
    <div class="{card_class}">
        <div class="metric-label">On Track?</div>
        <div class="metric-value">{icon} {status_text}</div>
        <div class="metric-sub">Gap: ₹{abs(results['gap']):.2f} CR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card-orange">
        <div class="metric-label">Expected by Day {days_passed}</div>
        <div class="metric-value">₹{results['expected_amount']:.2f} CR</div>
        <div class="metric-sub">{results['cumulative_expected_percentage']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

# Projection table
st.markdown('<div class="table-section">', unsafe_allow_html=True)
st.markdown('<div class="table-header">📈 Disbursement Projection for Upcoming Periods</div>', unsafe_allow_html=True)
st.markdown('<div class="table-content">', unsafe_allow_html=True)

if results["projection_data"]:
    df = pd.DataFrame(results["projection_data"])
    
    # Remove Historical % column
    df = df[["Period", "At Current Pace (CR)", "To Hit Target (CR)"]]
    
    # Style the dataframe
    styled_df = df.style.format({
        'At Current Pace (CR)': '₹{:.3f}',
        'To Hit Target (CR)': '₹{:.3f}'
    }).set_properties(**{
        'text-align': 'center'
    }).set_table_styles([
        {'selector': 'thead th', 'props': [
            ('background-color', '#1e293b'),
            ('color', '#94a3b8'),
            ('font-weight', '600'),
            ('text-align', 'center'),
            ('padding', '14px 12px'),
            ('border-bottom', '1px solid #475569')
        ]},
        {'selector': 'tbody td', 'props': [
            ('text-align', 'center'),
            ('padding', '14px 12px'),
            ('color', '#e2e8f0'),
            ('background-color', '#1e293b'),
            ('border-bottom', '1px solid #334155')
        ]},
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#334155')
        ]},
        {'selector': 'tbody tr:last-child td', 'props': [
            ('border-bottom', 'none')
        ]}
    ])
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
else:
    st.info("No upcoming periods to display.")

st.markdown('</div></div>', unsafe_allow_html=True)

# Alert message
if results["gap"] > 0:
    st.markdown(f"""
    <div class="alert-error">
        <h3>⚠ Alert: On Track to Miss Target</h3>
        <p>You are on track to disburse only <strong>₹{results['total_projected']:.2f} CR</strong>, 
        short by <strong>₹{results['gap']:.2f} CR</strong>. You need to increase disbursement in upcoming periods to 
        meet the target. The "To Hit Target" column shows what you should disburse in each period to achieve ₹{target_amount:.2f} CR.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-success">
        <h3>✓ On Track: Target Achievement Confirmed</h3>
        <p>At your current pace, you will exceed the target and potentially disburse 
        <strong>₹{results['total_projected']:.2f} CR</strong>. Great work! Continue maintaining this momentum.</p>
    </div>
    """, unsafe_allow_html=True)

import pandas as pd
import plotly.express as px

# -----------------------------
# LOAD DATA
# -----------------------------
df_trans = pd.read_csv("aggreated_transaction.csv")
df_top_ins = pd.read_csv("top_insurance.csv")
df_user = pd.read_csv("Top_user.csv")
df_district = pd.read_csv("district_registering_map.csv")

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
def clean(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

df_trans = clean(df_trans)
df_top_ins = clean(df_top_ins)
df_user = clean(df_user)
df_district = clean(df_district)

# -----------------------------
# HELPER: SAFE COLUMN FINDER
# -----------------------------
def find_col(df, options, name):
    for col in options:
        if col in df.columns:
            return col
    raise ValueError(f"{name} column not found. Available: {df.columns}")

# -----------------------------
# DETECT COLUMNS (AUTO)
# -----------------------------

# Transaction
state_col = find_col(df_trans, ["state"], "state")
year_col = find_col(df_trans, ["year"], "year")
quarter_col = find_col(df_trans, ["quarter", "quater"], "quarter")
txn_amount = find_col(df_trans, ["transaction_amount", "amount"], "transaction amount")
txn_count = find_col(df_trans, ["transaction_count", "count"], "transaction count")

# Insurance (district level)
ins_amount = find_col(df_top_ins, ["district_amount", "amount"], "insurance amount")

# User dataset
user_col = find_col(df_user,
    ["district_registered_users", "pincode_registered_users"],
    "user"
)

# District dataset
district_user = find_col(df_district, ["registered_user"], "district users")
app_open = find_col(df_district, ["app_opening"], "app opens")

# -----------------------------
# DATA PREPARATION
# -----------------------------

# Transactions
state_txn = df_trans.groupby(state_col)[txn_amount].sum().reset_index()
year_txn = df_trans.groupby(year_col)[txn_amount].sum().reset_index()
heat_txn = df_trans.groupby([state_col, quarter_col])[txn_count].sum().unstack(fill_value=0)

# Insurance
top_ins = df_top_ins.groupby("state")[ins_amount].sum().reset_index().sort_values(by=ins_amount, ascending=False)

# Users (state)
top_user = df_user.groupby("state")[user_col].sum().reset_index().sort_values(by=user_col, ascending=False)

# District users
district_users = df_district.groupby("district")[district_user].sum().reset_index()
user_growth = df_district.groupby("year")[district_user].sum().reset_index()
user_heat = df_district.groupby(["state", "quarter"])[app_open].sum().unstack(fill_value=0)

# -----------------------------
# CHARTS
# -----------------------------

fig1 = px.bar(state_txn, x=state_col, y=txn_amount,
              title="💰 Transaction Amount by State", color=txn_amount)

fig2 = px.line(year_txn, x=year_col, y=txn_amount,
               title="📈 Yearly Transaction Trend", markers=True)

fig3 = px.imshow(heat_txn,
                 title="🔥 Transaction Count Heatmap",
                 labels=dict(x="Quarter", y="State", color="Count"))

fig4 = px.bar(top_ins.head(10), x="state", y=ins_amount,
              title="🛡️ Top Insurance States", color=ins_amount)

fig5 = px.bar(top_user.head(10), x="state", y=user_col,
              title="👥 Top States by Users", color=user_col)

fig6 = px.bar(district_users.sort_values(by=district_user, ascending=False).head(10),
              x="district", y=district_user,
              title="🏙️ Top Districts by Users", color=district_user)

fig7 = px.line(user_growth, x="year", y=district_user,
               title="📈 User Growth Over Time", markers=True)

fig8 = px.imshow(user_heat,
                 title="🔥 App Opens Heatmap",
                 labels=dict(x="Quarter", y="State", color="App Opens"))

# -----------------------------
# HTML DASHBOARD
# -----------------------------
html = f"""
<html>
<head>
<title>PhonePe Dashboard</title>
<style>
body {{
    font-family: Arial;
    background-color: #0f172a;
    color: white;
}}
h1 {{
    text-align: center;
    color: #38bdf8;
}}
.section {{
    margin: 40px;
}}
</style>
</head>

<body>

<h1>📊 PhonePe Insights Dashboard</h1>

<div class="section">{fig1.to_html(full_html=False, include_plotlyjs='cdn')}</div>
<div class="section">{fig2.to_html(full_html=False, include_plotlyjs=False)}</div>
<div class="section">{fig3.to_html(full_html=False, include_plotlyjs=False)}</div>
<div class="section">{fig4.to_html(full_html=False, include_plotlyjs=False)}</div>
<div class="section">{fig5.to_html(full_html=False, include_plotlyjs=False)}</div>
<div class="section">{fig6.to_html(full_html=False, include_plotlyjs=False)}</div>
<div class="section">{fig7.to_html(full_html=False, include_plotlyjs=False)}</div>
<div class="section">{fig8.to_html(full_html=False, include_plotlyjs=False)}</div>

</body>
</html>
"""

# Save file
with open("dashboard1.html", "w") as f:
    f.write(html)

print("✅ FINAL Dashboard Created: dashboard.html")
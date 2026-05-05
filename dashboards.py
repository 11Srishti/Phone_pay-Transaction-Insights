
import pandas as pd
import json

# Loading all files
agg_ins = pd.read_csv("aggreated_insurance.csv")
agg_trans = pd.read_csv("aggreated_transaction.csv")
agg_user = pd.read_csv("aggreated_user.csv")
map_ins = pd.read_csv("map_insurance.csv")
map_trans = pd.read_csv("map_transaction.csv")
map_user = pd.read_csv("map_user.csv")
top_ins = pd.read_csv("top_insurance.csv")
top_trans = pd.read_csv("top_transaction.csv")
top_user = pd.read_csv("Top_user.csv")

# 1. Transaction Success Metrics (Aggregated)
trans_types = agg_trans.groupby('transaction_name').agg({'transaction_count': 'sum', 'transaction_amount': 'sum'}).reset_index()
# Calculate average transaction value per type
trans_types['avg_value'] = trans_types['transaction_amount'] / trans_types['transaction_count']

# 2. Regional Insurance Density (Map)
state_ins = map_ins.groupby('State')['insurance_count'].sum().sort_values(ascending=False).head(10)

# 3. User Brand Loyalty (Aggregated)
brand_data = agg_user.groupby('brand')['count'].sum().sort_values(ascending=False).head(8)

# 4. Pincode Heatmap Data (Top)
pincode_activity = top_trans.groupby('entity_name_pincodes')['count_pincode'].sum().sort_values(ascending=False).head(10)

# 5. Device Usage Percentage over time
brand_time = agg_user.groupby(['Year', 'brand'])['percentage'].mean().unstack().fillna(0).to_dict()

# Packaging data for JS
dashboard_data = {
    "trans_types": trans_types['transaction_name'].tolist(),
    "trans_avg_values": trans_types['avg_value'].tolist(),
    "state_ins_labels": state_ins.index.tolist(),
    "state_ins_values": state_ins.values.tolist(),
    "brand_labels": brand_data.index.tolist(),
    "brand_values": brand_data.values.tolist(),
    "pincode_labels": [str(int(p)) for p in pincode_activity.index.tolist()],
    "pincode_values": pincode_activity.values.tolist()
}

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Advanced Financial Ecosystem Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 1200px; margin: auto; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }}
        h1 {{ text-align: center; color: #38bdf8; margin-bottom: 40px; font-weight: 300; }}
        h2 {{ font-size: 1.1rem; margin-bottom: 20px; color: #94a3b8; border-left: 4px solid #38bdf8; padding-left: 10px; }}
        .full-width {{ grid-column: span 2; }}
        canvas {{ width: 100% !important; height: 300px !important; }}
    </style>
</head>
<body>
    <h1>Financial Intelligence Operations Center</h1>
    
    <div class="grid">
        <div class="card">
            <h2>Average Transaction Value by Type</h2>
            <canvas id="avgTransChart"></canvas>
        </div>
        
        <div class="card">
            <h2>Insurance Penetration by State (Top 10)</h2>
            <canvas id="insStateChart"></canvas>
        </div>

        <div class="card">
            <h2>User Device Distribution (Brand Share)</h2>
            <canvas id="brandChart"></canvas>
        </div>

        <div class="card">
            <h2>Top 10 Active Pincodes (Transaction Volume)</h2>
            <canvas id="pincodeChart"></canvas>
        </div>
    </div>

    <script>
        const d = {json.dumps(dashboard_data)};
        
        const chartOptions = {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
            scales: {{ 
                y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8' }} }}
            }}
        }};

        // Avg Transaction Value
        new Chart(document.getElementById('avgTransChart'), {{
            type: 'bar',
            data: {{
                labels: d.trans_types,
                datasets: [{{
                    label: 'Avg Value (INR)',
                    data: d.trans_avg_values,
                    backgroundColor: '#38bdf8'
                }}]
            }},
            options: chartOptions
        }});

        // Insurance by State
        new Chart(document.getElementById('insStateChart'), {{
            type: 'line',
            data: {{
                labels: d.state_ins_labels,
                datasets: [{{
                    label: 'Policies Issued',
                    data: d.state_ins_values,
                    borderColor: '#fbbf24',
                    backgroundColor: 'rgba(251, 191, 36, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: chartOptions
        }});

        // Brand Pie
        new Chart(document.getElementById('brandChart'), {{
            type: 'doughnut',
            data: {{
                labels: d.brand_labels,
                datasets: [{{
                    data: d.brand_values,
                    backgroundColor: ['#f472b6', '#818cf8', '#34d399', '#fb7185', '#a78bfa', '#22d3ee', '#fb923c', '#94a3b8']
                }}]
            }},
            options: {{ ...chartOptions, scales: {{}} }} // No scales for doughnut
        }});

        // Pincode Volume
        new Chart(document.getElementById('pincodeChart'), {{
            type: 'bar',
            data: {{
                labels: d.pincode_labels,
                datasets: [{{
                    label: 'Total Transactions',
                    data: d.pincode_values,
                    backgroundColor: '#818cf8'
                }}]
            }},
            options: {{ ...chartOptions, indexAxis: 'y' }}
        }});
    </script>
</body>
</html>
"""

with open("advanced_dashboard.html", "w") as f:
    f.write(html_content)

print("Advanced dashboard saved as 'advanced_dashboard.html'.")






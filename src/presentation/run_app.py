import streamlit as st

st.set_page_config(page_title="FinanceAI", page_icon="🏠", layout="wide")

homepage = st.Page(
    "views/1_🏠_Homepage.py",
    title="Homepage",
    icon="🏠",
    default=True
)

transactions = st.Page(
    "views/2_💳_My_Transactions.py",
    title="My Transactions",
    icon="💳"
)

charts = st.Page(
    "views/3_📊_Chart_Analysis.py",
    title="Chart Analysis",
    icon="📊"
)

assistant = st.Page(
    "views/4_🤖_AI_Assistant.py",
    title="AI Assistant",
    icon="🤖"
)

data = st.Page(
    "views/5_📁_Data_Management.py",
    title = "Data Management",
    icon = "📁"
)

if "system_ready" not in st.session_state:
    st.session_state.system_ready = False

if not st.session_state.system_ready:
    pg = st.navigation({"": [homepage, data]})
else:
    pg = st.navigation({"": [homepage, transactions, charts, assistant, data]})

pg.run()
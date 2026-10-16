# Simple personal finance dashboard built with Streamlit, pandas, and Altair
import streamlit as st
import pandas as pd
import altair as alt


@st.cache_data
def load_and_clean_data(path: str) -> pd.DataFrame:
    """
    Load transactions data from CSV and perform basic cleaning.
    """
    data = pd.read_csv(path)
    data['Type'] = data['Type'].str.strip().str.lower()
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date'])
    data = data.sort_values('Date')
    return data


st.set_page_config(page_title="Personal Finance Dashboard", layout="centered")

#title and description
st.title("Personal Finance Dashboard")
st.caption("A simple dashboard to explore income, expenses, and balance from a CSV file.")

#sidebar filters
# Filters allow users to interactively subset the data by date and category


data = load_and_clean_data("transactions.csv")
min_date = data['Date'].min()
max_date = data['Date'].max()
start_date, end_date = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
filtered_data = data[
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date))
]
categories = st.sidebar.multiselect(
    "Categories",
    options=sorted(filtered_data['Category'].unique()),
    default=sorted(filtered_data['Category'].unique())
)
filtered_data = filtered_data[
    filtered_data['Category'].isin(categories)
].copy()

if filtered_data.empty:
    st.warning("No data for selected filters.")
    st.stop()


#main dashboard
st.header("Data Overview")
st.dataframe(filtered_data)

#summary metrics
total_income = filtered_data[filtered_data['Type'] == 'income']['Amount'].sum()
total_expense = filtered_data[filtered_data['Type'] == 'expense']['Amount'].sum()
st.metric("Number of Transactions", len(filtered_data))
balance = total_income - total_expense

st.divider()

st.subheader("Financial Summary")
st.metric("Total Income", f"£{total_income:,.2f}")
st.metric("Total Expense", f"£{total_expense:,.2f}")
st.metric("Balance", f"£{balance:,.2f}")

avg_transaction = filtered_data['Amount'].mean()
st.metric("Average Transaction", f"£{avg_transaction:,.2f}")

st.divider()

#visualisations
st.markdown("---")
st.header("Visualisations Overview")
st.subheader("Spending by category")
chart = alt.Chart(filtered_data[filtered_data['Type'] == 'expense']).mark_bar().encode(
    x=alt.X('Category', sort='-y'),
    y=alt.Y('Amount', axis=alt.Axis(format='£,.0f')),
)
st.altair_chart(chart, use_container_width=True)
st.subheader("Income by category")
chart_income = alt.Chart(filtered_data[filtered_data['Type'] == 'income']).mark_bar().encode(
    x=alt.X('Category', sort='-y'),
    y=alt.Y('Amount', axis=alt.Axis(format='£,.0f')),
)

st.altair_chart(chart_income, use_container_width=True)

st.subheader("Balance Over Time")
signed_amount = filtered_data['Amount'].where(
    filtered_data['Type'] == 'income',
    -filtered_data['Amount']
)
filtered_data['Balance'] = signed_amount.cumsum()
st.line_chart(filtered_data.set_index('Date')['Balance'], use_container_width=True)
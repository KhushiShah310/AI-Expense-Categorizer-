import streamlit as st
import pandas as pd
from categorizer import categorize_transactions

st.title("AI Expense Categorizer")
st.write("Upload your bank transactions and let AI categorize them for you.")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Your Transactions")
    st.dataframe(df)
    
    if st.button("Categorize with AI"):
        with st.spinner("Claude is categorizing your transactions..."):
            df["category"] = categorize_transactions(df)
        
        st.subheader("Categorized Transactions")
        st.dataframe(df)
        
        st.subheader("Monthly Spending by Category")
        summary = df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(summary.set_index("category"))
        
        st.subheader("Category Totals")
        for _, row in summary.iterrows():
            st.metric(label=row["category"], value=f"${row['amount']:.2f}")
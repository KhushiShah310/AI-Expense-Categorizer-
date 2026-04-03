import streamlit as st
import pandas as pd
from categorizer import categorize_transactions, extract_from_receipt

st.title("AI Expense Categorizer")
st.write("Upload your bank transactions and let AI categorize them for you.")

tab1, tab2 = st.tabs(["CSV Upload", "Receipt Photo"])

with tab1:
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

with tab2:
    receipt = st.file_uploader("Upload a receipt photo", type=["jpg", "jpeg", "png"])
    
    if receipt is not None:
        st.image(receipt, caption="Your receipt", width=300)
        
        if st.button("Extract with AI"):
            with st.spinner("Claude is reading your receipt..."):
                result = extract_from_receipt(receipt.read())
            
            st.success("Done!")
            st.write(result)
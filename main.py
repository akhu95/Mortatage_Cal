import streamlit as st
import pandas as pd
import math

st.title('Mortage Calculator')

st.write('## Input data')
col1,col2 = st.columns(2)
home_value = col1.number_input("Home Value",min_value=0,value=500000)
deposit_value = col2.number_input("Deposit Value",min_value=0,value=50000)
int_rate= col1.number_input("Interest Rate in (%)",min_value=0.0,value=5.5)
Term = col2.number_input("Loan term in years",min_value=1,value=5)

# calculate payments

loan_amount = home_value - deposit_value
monthly_int_rate = (int_rate/100)/12
number_of_payments = Term*12
monthly_payments =  (
    loan_amount * 
    (monthly_int_rate * (1 + monthly_int_rate) ** number_of_payments)/
    ((1 + monthly_int_rate) ** number_of_payments - 1)
)

total_payment=monthly_payments*number_of_payments
total_interest=total_payment-loan_amount

st.write("### Repayments")
col1,col2,col3=st.columns(3)
col1.metric(label="Monthly Repayments",value=f"Rs.{monthly_payments:,.2f}")
col2.metric(label="Total Payment",value=f"Rs.{total_payment:,.0f}")
col3.metric(label="Total Interest",value=f"Rs.{total_interest:,.0f}")

#create scheudle

schedule=[]
remaining_bal = loan_amount

for i in range(1, number_of_payments+1):
    interest_payment = remaining_bal*monthly_int_rate
    principal_payment = monthly_payments-interest_payment
    remaining_bal -=principal_payment
    year=math.ceil(i/12)
    schedule.append(
    [
        i,
        monthly_payments,
        principal_payment,
        interest_payment,
        remaining_bal,
        year,
    ]
    )
df=pd.DataFrame (schedule,columns=['Month','Payment','Principal','Interest','Remianing Balance','Year'])

#display dataframe as chart

st.write("### Payment Schedule")
payments_df = df[['Year','Remianing Balance']].groupby('Year').min()
st.line_chart(payments_df)

'''
credit_policy: 1 if the customer meets the credit underwriting 
criteria of LendingClub.com, and 0 otherwise.

purpose：贷款人贷款的用途

int_rate：贷款的利率

installment：分期付款，每期还款的额度

log_annual_inc: The natural log of the annual income of the borrower.

dti: The debt-to-income ratio of the borrower. 
借款人的债务收入比。

fico: The FICO credit score of the borrower.
借款人的 FICO 信用评分。

days_with_cr_line: The number of days the borrower has had a credit line.
借款人拥有信用额度的天数。

revol_bal: The borrower’s revolving balance.
借款人的余额。

revol_util: The borrower’s revolving line utilization rate.
借款人的循环线利用率。

inq_last_6mths: The borrower’s number of inquiries by creditors in the last 6 months.
借款人最近6个月的债权人查询次数。

delinq_2yrs: The number of times the borrower had been 30+ days past due on a payment in the past 2 years.
借款人在过去 2 年内逾期 30 天以上的付款次数。

pub_rec: The borrower’s number of derogatory public records.
借款人的贬损公共记录的数量。

not_fully_paid: indicates whether the loan was not paid back in full (the borrower either defaulted or the borrower was deemed unlikely to pay it back).
表示贷款是否未全额偿还（借款人违约或借款人被认为不太可能偿还）
'''


import pickle
import streamlit as st
from PIL import Image
import numpy as np
import math
import pandas as pd
import time

def app():

    st.markdown("<h1 style='text-align: center; color: black;'>Would you pay off the loan?</h1>", unsafe_allow_html=True)
    st.markdown(' --- ')
    
    @st.cache(allow_output_mutation=True)
    def openModel():
        model  = pickle.load(open('model/lc.model', 'rb'))
        return model
    model = openModel()
    
    @st.cache(allow_output_mutation=True)
    def openPipeline():
        pipeline = pickle.load(open('model/feature.pipeline', 'rb'))
        return pipeline
    
    model = openModel()
    pipeline = openPipeline()

    # header_pic = Image.open('header.jpg')
    # st.image(header_pic, use_column_width=True)



    def creditPolicy(credit_policy_choice):
        if credit_policy_choice == "You can meets the credit underwriting criteria":
            return 1
        else:
            return 0

    # credit_policy
    credit_policy_option = ["You can meets the credit underwriting criteria", "You cannot meets the credit underwriting criteria"]
    credit_policy_choice = st.selectbox("Which credit policy would you prefer?", options=credit_policy_option)
    st.write('You selected:', credit_policy_choice)

    credit_policy = creditPolicy(credit_policy_choice)
    st.markdown(' --- ')

    # purpose
    purpose_list = ['debt_consolidation', 'credit_card', 'all_other',
        'home_improvement', 'small_business', 'major_purchase',
        'educational']

    purpose = st.selectbox("What is your purpose of the loan?", options=purpose_list)
    st.write('You selected:', purpose)

    st.markdown(' --- ')

    # int_rate
    int_rate = st.number_input("What is your interest rate of the loan (proportion)?", value=0.005, step=0.001)
    st.write('You selected:', int_rate)

    st.markdown(' --- ')

    # installment
    installment = st.number_input("What is your monthly installments (10$ - 1000$)?", value=50, step=1, max_value=1000, min_value=10)
    st.write('You selected:', installment)
    st.markdown(' --- ')

    # log annual income
    annual_income = st.number_input("What is your annual income (1$ ~)?", value=50, step=1, min_value=1)
    st.write('You selected:', annual_income)
    # 求自然底数
    log_annual_income = round(math.log(annual_income), 5)
    st.markdown(' --- ')

    # dti 债务收入比
    dti = st.number_input("What is your debt-to-income ratio (0 - 50)?", value=5, step=1, max_value=50, min_value=0)
    st.write('You selected:', dti)
    st.markdown(' --- ')

    # fico 信用评级
    fico = st.number_input("What is your FICO credit score (600 - 800)?", value=600, step=1, max_value=850, min_value=600)
    st.write('You selected:', fico)
    st.markdown(' --- ')

    # days_with_cr_line 借款人拥有信用额度的天数
    days_with_cr_line = st.number_input("What is the number of days you has had a credit line (100 - 18000)?", value=100, step=1, max_value=18000, min_value=100)
    st.write('You selected:', days_with_cr_line)
    st.markdown(' --- ')

    # revol_bal Revolving Balance 。
    revol_bal = st.number_input("What is your revolving balance (0 - 120000)?", value=1, step=1, max_value=120000, min_value=0)
    st.write('You selected:', revol_bal)
    st.markdown(' --- ')

    # revol_util
    revol_util = st.number_input("What is your credit utilization ratio (0 - 120)?", value=1, step=1, max_value=120, min_value=0)
    st.write('You selected:', revol_util)
    st.markdown(' --- ')

    # inq_last_6mths
    inq_last_6mths = st.number_input("What is your number of inquiries by creditors in the last 6 months (0 - 30)?", value=1, step=1, max_value=30, min_value=0)
    st.write('You selected:', inq_last_6mths)
    st.markdown(' --- ')

    # delinq_2yrs
    delinq_2yrs = st.number_input("What is the number of times you had been 30+ days past due on a payment in the past 2 years (0 - 15)?", value=0, step=1, max_value=15, min_value=0)
    st.write('You selected:', delinq_2yrs)
    st.markdown(' --- ')

    # pub_rec
    pub_rec = st.number_input("What is your number of derogatory public records (0 - 5)?", value=1, step=1, max_value=5, min_value=0)
    st.write('You selected:', pub_rec)
    st.markdown(' --- ')

    feature = {
            'credit_policy': credit_policy,
            'purpose': purpose, 
            'int_rate': int_rate, 
            'installment': installment, 
            'log_annual_income': log_annual_income, 
            'dti': dti, 
            'fico': fico,
            'days_with_cr_line': days_with_cr_line, 
            'revol_bal': revol_bal,
            'revol_util': revol_util,
            'inq_last_6mths': inq_last_6mths, 
            'delinq_2yrs': delinq_2yrs, 
            'pub_rec': pub_rec}

    # 点击预测
    if st.button("Click to predict Whether your Loan Will Go Bad"):

        
        feature_df = pd.DataFrame(feature, index=[0])
        st.dataframe(feature_df)
        
        X_test_features = pipeline.transform(feature_df)
        prediction = model.predict(X_test_features)
        
        with st.spinner('Processing...'):
            time.sleep(2)
        st.success('Done!')
        
        if prediction == 1:
            # st.image(survived_pic, use_column_width=True)
            st.write("你老赖了")

        else:
            # st.image(death_pic, use_column_width=True)
            st.write("你能还清贷款")
        
    
    
    
    
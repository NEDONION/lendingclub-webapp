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

    st.markdown("<h1 style='text-align: center;'>Loan Eligibility Assessment</h1>", unsafe_allow_html=True)
    # 手动换行
    st.markdown("  ")
    st.markdown("  ")
    
    header1, header_null, header2 = st.columns([4, 0.3, 5])
    with header1:
        bank = Image.open("img/bank.jpg")
        st.image(bank)
    
    with header2:
        st.markdown("<h3 style='color:#F63366;'><b>Introduction<b></h3>", unsafe_allow_html=True)
        st.write(
    """
    文案1:
      - 文案2
      - 文案2
    """
        )
    
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

    col1, col2 = st.columns(2)
    with col1:
        st.write(
    """
    #### **Enter Personal Details:**
    """)   
    
    with col2:
        st.write(
    """
    #### **Enter Loan Details:**
    """)   
    
    st.markdown(" --- ")
    
    col3, col4= st.columns(2)
    
    with col3:
        st.write(
    """
    #### **Enter Credit Report:**
    """)   
        
    with col4:
        st.write(
    """
    #### **Enter Past Records:**
    """)   
    
    
    yourname = col1.text_input("Your Name")

    def creditPolicy(credit_policy_choice):
        if credit_policy_choice == "Meet the credit policy":
            return 1
        else:
            return 0

    # credit_policy
    credit_policy_option = ["Meet the credit policy", "Does not meet the credit policy"]
    credit_policy_help = "If the customer meets the credit underwriting criteria of LendingClub.com"
    credit_policy_choice = col1.selectbox("Credit Policy", options=credit_policy_option, help=credit_policy_help)
    credit_policy = creditPolicy(credit_policy_choice)

    # purpose
    purpose_list = ['debt_consolidation', 'credit_card', 'all_other',
        'home_improvement', 'small_business', 'major_purchase',
        'educational']
    purpose = col1.selectbox("Loan Purpose", options=purpose_list)

    # log annual income
    annual_income = col1.number_input("Annual Income (1$ ~)", value=50, step=1, min_value=1)
    # 求自然底数
    log_annual_inc = round(math.log(annual_income), 5)


    int_rate = col2.number_input("Interest Rate (0.05 - 0.25)?", value=0.05, step=0.01)
    
    installment_help = "The monthly installments ($) owed by the borrower if the loan is funded."
    installment = col2.number_input("Monthly Installments (10$ - 1000$)", value=50, step=1, max_value=1000, min_value=10, help=installment_help)
    
    revol_bal = col2.number_input("Revolving Balance (0 - 120000)", value=1, step=1, max_value=120000, min_value=0)
    revol_util = col2.number_input("Credit Utilization Ratio (0 - 120)", value=1, step=1, max_value=120, min_value=0)



    # dti 债务收入比
    dti = col3.number_input("Debt to Income Ratio (0 - 50)", value=5, step=1, max_value=50, min_value=0)
    # fico 信用评级
    fico = col3.number_input("FICO Credit Score (600 - 850)", value=600, step=1, max_value=850, min_value=600)
    # days_with_cr_line 借款人拥有信用额度的天数
    days_with_cr_line = col3.number_input("Number of days You has had a credit line (100 - 18000)", value=100, step=1, max_value=18000, min_value=100)


    # inq_last_6mths
    inq_last_6mths = col4.number_input("Number of Inquiries by creditors in the last 6 months (0 - 30)", value=1, step=1, max_value=30, min_value=0)
    # delinq_2yrs
    delinq_2yrs = col4.number_input("Number of times You had been 30+ days past due on a payment (0 - 15)", value=0, step=1, max_value=15, min_value=0)
    # pub_rec
    pub_rec = col4.number_input("Number of Derogatory Public Records (0 - 5)", value=1, step=1, max_value=5, min_value=0)

    
    st.markdown(" --- ")
    feature = {
            'credit_policy': credit_policy,
            'purpose': purpose, 
            'int_rate': int_rate, 
            'installment': installment, 
            'log_annual_inc': log_annual_inc, 
            'dti': dti, 
            'fico': fico,
            'days_with_cr_line': days_with_cr_line, 
            'revol_bal': revol_bal,
            'revol_util': revol_util,
            'inq_last_6mths': inq_last_6mths, 
            'delinq_2yrs': delinq_2yrs, 
            'pub_rec': pub_rec}

    # 点击预测
    if st.button("Check Eligibility"):

        
        feature_df = pd.DataFrame(feature, index=[0])
        # st.dataframe(feature_df)
        
        X_test_features = pipeline.transform(feature_df)
        prediction = model.predict(X_test_features)
        
        with st.spinner('Processing...'):
            time.sleep(1)
        st.success('Done!')
        
        if prediction == 1:
            # st.image(survived_pic, use_column_width=True)
            st.warning(f"{yourname}你老赖了")

        else:
            # st.image(death_pic, use_column_width=True)
            st.success(f"Congratulations {yourname}! Based on the information you provided, You're eligible for the Loan.")
        
    
    
    
    
import streamlit as st


def app():
    
    # add space function.
    def space(n):
        for i in range(n):
            st.markdown("  ")
            
    # html语法设置主页
    st.markdown("<h1 style='text-align: center; font-size:65px;'>&#128181;</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; '>Borrow Faster</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; font-size:20px;'>Application to determine your Loan Eligibility.</h3>", 
                unsafe_allow_html=True)
    
    
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>What is this App about?<b></h3>", unsafe_allow_html=True)
    st.write('''
             Whether you want to borrow money to buy real estate, cars or to open up a start-up, **Borrow Faster** offers a quick credit evaluation to help you judge whether you are eligible for the Lending Club loan application. With a user-friendly interface, and offering many evaluation models for loan applicants.
             ''')
    
    space(1)
   
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>Who is this App for?<b></h3>", unsafe_allow_html=True)
    st.write('''
             - If you are an individual applicant, fill out our application form to check whether you can pass the loan evaluation. 
             - If you have an applicants’ list, bring up your applicants’ information (.csv file) and upload it to our model to check how many of your applicants can pass the loan application evaluation, namely, the proportion of whom will make full payments on time.
             ''')   
    
    space(1)
    
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>About the data set<b></h3>", unsafe_allow_html=True)
    st.write('''
             Lending Club is a peer-to-peer lending company that matches borrowers with investors through an online platform. It services people that need personal loans between $1,000 and $40,000. Borrowers receive the full amount of the issued loan minus the origination fee, which is paid to the company. Investors purchase notes backed by the personal loans and pay Lending Club a service fee. The company shares data about all loans issued through its platform during certain time periods.
             **We choose the Lending Club data set with 13 columns:**
             ''')
    st.write('''
             - **credit_policy**: 1 if the customer meets the credit underwriting criteria of LendingClub.com, and 0 otherwise.
             - **purpose**: The purpose of the loan such as: credit_card, debt_consolidation, etc.
             - **int_rate**: The interest rate of the loan (proportion).
             - **installment**: The monthly installments ($) owed by the borrower if the loan is funded.
             - **log_annual_inc**: The natural log of the annual income of the borrower.
             - **dti**: The debt-to-income ratio of the borrower.
             - **fico**: The FICO credit score of the borrower.
             - **days_with_cr_line**: The number of days the borrower has had a credit line.
             - **revol_bal**: The borrower’s revolving balance.
             - **revol_util**: The borrower’s revolving line utilization rate.
             - **inq_last_6mths**: The borrower’s number of inquiries by creditors in the last 6 months.
             - **delinq_2yrs**: The number of times the borrower had been 30+ days past due on a payment in the past 2 years.
             - **pub_rec**: The borrower’s number of derogatory public records.
             - **not_fully_paid**: indicates whether the loan was not paid back in full (the borrower either defaulted or the borrower was deemed unlikely to pay it back.
             ''')
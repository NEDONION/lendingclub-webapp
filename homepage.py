import streamlit as st


def app():
    # html语法设置主页
    st.markdown("<h1 style='text-align: center; '>Borrow Faster</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center; font-size:56px;'<p>&#129302;</p></h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; font-size:20px;'>Application to determine your Loan Eligibility.</h3>", 
                unsafe_allow_html=True)
    
    
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>What is this App about?<b></h3>", unsafe_allow_html=True)
    st.write('''
             Whether you want to borrow money to buy real estate, cars or to open up a start-up, **Borrow Faster** offers a quick credit evaluation to help you judge whether you are eligible for the Lending Club loan application. With a user-friendly interface, and offering many evaluation models for loan applicants.
             ''')
   
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:24px;'><b>Who is this App for?<b></h3>", unsafe_allow_html=True)
    st.write('''
             - If you are an individual applicant, fill out our application form to check whether you can pass the loan evaluation. 
             ''')
    st.write('''
             - If you have an applicants’ list, bring up your applicants’ information (.csv file) and upload it to our model to check how many of your applicants can pass the loan application evaluation, namely, the proportion of whom will make full payments on time.
             ''')     
    
    
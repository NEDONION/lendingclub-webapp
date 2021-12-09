import streamlit as st


def app():
    # html语法设置主页
    st.markdown("<h1 style='text-align: center; '>Welcome to LendingClub!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size:56px;'<p>&#129302;</p></h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey; font-size:20px;'>测试！</h3>", 
                unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>What is this App about?<b></h3>", unsafe_allow_html=True)
    st.write("测试1")
    st.write("测试1")     
    st.markdown("<h3 style='text-align: left; color:#F63366; font-size:18px;'><b>Who is this App for?<b></h3>", unsafe_allow_html=True)
    st.write("测试2")
    st.write("测试2")     
    
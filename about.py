import streamlit as st
from PIL import Image


def app():
    st.title('About Us')
    st.markdown(' --- ')
    st.write('We are a team of 5 members, focusing on building a  model to predict whether a loan will be fully-paid.')
    st.subheader('Team')
    
    jiacheng = Image.open('img/jiachenghu.png')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(jiacheng)
    with col2: 
        st.write('Jiacheng Hu')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(jiacheng)
    with col2: 
        st.write('Jiaquan Zhang')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(jiacheng)
    with col2: 
        st.write('Kechun Yang')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(jiacheng)
    with col2: 
        st.write('Yifan Xue')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(jiacheng)
    with col2: 
        st.write('Yuchuan Han')
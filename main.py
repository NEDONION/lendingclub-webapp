
import streamlit as st
import personalPredict
import homepage
import uploadPredict
import awsPredict
from multiapp import MultiApp
from PIL import Image

#############
#PAGE SET UP
#############

# ICON = Image.open("img/icon2.png")

st.set_page_config(
page_title="Welcome to Borrow Faster!",
page_icon= ":dollar:",
layout="wide",
initial_sidebar_state="expanded",
menu_items={
}
)


app = MultiApp()
app.add_app("Home Page", homepage.app)
app.add_app("Loan Eligibility Assessment", personalPredict.app)
app.add_app("Upload CSV to More Models", uploadPredict.app)
app.add_app("Connect to AWS Service", awsPredict.app)
app.run()

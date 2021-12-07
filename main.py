
import streamlit as st
import personalPredict
import homepage
import uploadButton
import about
from multiapp import MultiApp
from PIL import Image

#############
#PAGE SET UP
#############

# ICON = Image.open("img/icon2.png")

st.set_page_config(
page_title="Welcome to LendingClub!",
page_icon= ":dog:",
# layout="wide",
initial_sidebar_state="expanded",
menu_items={
'Get Help': 'https://www.extremelycoolapp.com/help',
'Report a bug': "https://www.extremelycoolapp.com/bug",
'About': "# This is a header. This is an *extremely* cool app!"
}
)


app = MultiApp()
app.add_app("Home Page", homepage.app)
app.add_app("Predict by Yourself", personalPredict.app)
# app.add_app("Upload CSV to Predict", uploadButton.app)
app.add_app("About us", about.app)
app.run()

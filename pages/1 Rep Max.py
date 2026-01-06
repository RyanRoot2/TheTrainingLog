import streamlit as st
from src.core.login import enforce_login
st.set_page_config(layout="wide")
enforce_login() # Auth check on every page

st.info("👋 This page will let you enter 1 RMs for any movement you want to track, \
        it will be used to auto-calculate weights for programs using the % 1RM option, \
        and it will keep track of estimated 1 RMs in the future, based on your logged workouts.")

st.info("... There's also a previous project I worked on that would calculate your percentile versus the Open Powerlifting database, \
        so if you want to see how weak you really are, I might add that here too :)")
import streamlit as st
import pandas as pd
from src.ui.components.program_builder_dimensions import get_program_dimensions
from src.ui.navigation import render_program_builder_tabs


st.title("Program Builder")
st.set_page_config(layout="wide")



render_program_builder_tabs()

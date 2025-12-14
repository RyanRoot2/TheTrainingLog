import streamlit as st
from src.ui.screens.mobile_week_select import render_mobile_week_select
from src.ui.screens.mobile_day_select import render_mobile_day_select
from src.ui.screens.mobile_day_view import render_mobile_day_view
from src.ui.screens.active_program_tab import render_active_program_tab
from src.ui.screens.program_library_tab import render_program_library_tab
from src.ui.screens.desktop_program_builder import render_desktop_program_builder

# --- Functions to navigate between screens ---

def render_current_screen():
    if st.session_state.current_screen == 'week_select':
        render_mobile_week_select()

    elif st.session_state.current_screen == 'day_select':
        render_mobile_day_select()
        
    elif st.session_state.current_screen == 'day_view':
        render_mobile_day_view()


def render_main_dashboard_tabs():
    active_program, program_library, program_bulder = st.tabs([
        "Active Program",
        "Program Library",
        "Program Builder"
    ])
    with active_program:
        render_active_program_tab()
    with program_library:
        render_program_library_tab()
    with program_bulder:
        st.page_link("pages/Program Builder.py", label='Take me to the Program Builder ➡️')


def render_program_builder_tabs():
    mobile, desktop, settings = st.tabs([
        "Mobile",
        "Desktop",
        "Settings"
    ])
    with mobile:
        st.subheader('Mobile')
    with desktop:
        if st.session_state.desktop_builder_step2 is True:
            st.dataframe(st.session_state.program_builder_data_step1)
        else:
            render_desktop_program_builder()
    with settings:
        st.subheader('Settings')
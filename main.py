import json
import os
import streamlit as st

st.set_page_config(layout="wide", page_title="BAAC Analytics")

from src.views import home, dataset, analysis, conclusion, login, logout, profile
from src.router import get_route
from PATHS import NAVBAR_PATHS, SETTINGS
import utils as utl

utl.inject_custom_css()

# ... (garder render_navbar) ...

def load_session() -> dict:
    # Sur le cloud, on utilise exclusivement st.session_state
    email = st.session_state.get("user_email", "")
    return {"email": email}

def navigation():
    session_data = load_session()
    email = session_data.get("email", "")

    route = get_route()

    if not email:
        login.load_view()
        return

    utl.navbar_component()

    if route == "/dataset":
        dataset.load_view()
    elif route == "/analysis":
        analysis.load_view()
    elif route == "/conclusion":
        conclusion.load_view()
    elif route == "/profile":
        profile.load_view()
    elif route == "/logout":
        logout.load_view()
    else:
        home.load_view()

navigation()
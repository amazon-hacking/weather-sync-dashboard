import streamlit as st
from sqlalchemy import create_engine

def get_engine():
    db_config = st.secrets["tembo_db"]
    username = db_config["username"]
    password = db_config["password"]
    host = db_config["host"]
    port = db_config["port"]
    database = db_config["database"]

    return create_engine(f"postgresql://{username}:{password}@{host}/{database}")

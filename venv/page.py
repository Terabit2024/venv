import streamlit as st
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the table
hosts = Table(
    'hosts', metadata,
    Column('id', Integer, primary_key=True),
    Column('host_name', String, nullable=False),
    Column('date', Date, nullable=False),
    Column('excluded', String, nullable=False)
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Authentication
def authenticate(username, password):
    # Simple authentication logic (replace with your own)
    return username == "admin" and password == "password"

# Streamlit app
st.title("Streamlit App with Authentication")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Logged in successfully")
        else:
            st.error("Invalid username or password")
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Insert Data", "Logout"])

    if page == "Insert Data":
        st.header("Insert Data into Database")
        host_name = st.text_input("Host Name")
        date = st.date_input("Date", datetime.now())
        excluded = st.text_input("Excluded")

        if st.button("Submit"):
            new_host = hosts.insert().values(
                host_name=host_name,
                date=date,
                excluded=excluded
            )
            session.execute(new_host)
            session.commit()
            st.success("Data inserted successfully")

    elif page == "Logout":
        st.session_state.authenticated = False
        st.success("Logged out successfully")
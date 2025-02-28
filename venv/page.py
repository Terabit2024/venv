import streamlit as st
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime

st.set_page_config(page_title="Ndejat")

# Database setup
DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the tables
hosts = Table(
    'hosts', metadata,
    Column('id', Integer, primary_key=True),
    Column('host_name', String, nullable=False),
    Column('date', Date, nullable=False),
    Column('excluded', String, nullable=False)
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False, unique=True),
    Column('password', String, nullable=False)
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Authentication
def authenticate(username, password):
    user = session.query(users).filter_by(username=username, password=password).first()
    if user:
        return True
    return False

# User registration function
def register_user(username, password):
    existing_user = session.query(users).filter_by(username=username).first()
    if existing_user:
        return False, "Username already exists"
    new_user = users.insert().values(username=username, password=password)
    session.execute(new_user)
    session.commit()
    return True, "User registered successfully"

# Streamlit app
st.title("Ndejat")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    page = st.sidebar.radio("Go to", ["Login", "Sign Up"])
    if page == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.rerun()
                st.success("Kycja u krye me sukses")
            else:
                st.error("Invalid username or password")
    elif page == "Sign Up":
        st.header("Sign Up")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            success, message = register_user(new_username, new_password)
            if success:
                st.success(message)
                st.session_state.authenticated = False
                st.set_query_params()
            else:
                st.error(message)
else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Logout"])

    if page == "Home":
        st.header("Inserto te dhena")
        host_name = st.text_input("Mikpritesi")
        date = st.date_input("Data", datetime.now())
        excluded = st.text_input("Perjashtuar")

        if st.button("Ruaj"):
            new_host = hosts.insert().values(
                host_name=host_name,
                date=date,
                excluded=excluded
            )
            session.execute(new_host)
            session.commit()
            st.success("Te dhena u ruajten me sukses")

        st.header("Lista e Mikpritesve")
        host_list = session.query(hosts).all()
        if host_list:
            st.table([{ "ID": host.id, "Mikpritesi": host.host_name, "Data": host.date, "Perjashtuar": host.excluded } for host in host_list])
        else:
            st.write("Nuk ka te dhena")

        if 'edit_host_id' in st.session_state:
            st.header("Edito Mikpritesin")
            host_to_edit = session.query(hosts).filter_by(id=st.session_state.edit_host_id).first()
            new_host_name = st.text_input("Mikpritesi", value=host_to_edit.host_name)
            new_date = st.date_input("Data", value=host_to_edit.date)
            new_excluded = st.text_input("Perjashtuar", value=host_to_edit.excluded)

            if st.button("Update"):
                session.query(hosts).filter_by(id=st.session_state.edit_host_id).update({
                    'host_name': new_host_name,
                    'date': new_date,
                    'excluded': new_excluded
                })
                session.commit()
                st.success("Mikpritesi u perditesua me sukses")
                del st.session_state.edit_host_id
                st.rerun()

    elif page == "Logout":
        st.session_state.authenticated = False
        st.success("Ckyqja u krye me sukses")
        st.query_params()
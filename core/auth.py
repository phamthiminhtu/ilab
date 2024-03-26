
import streamlit as st
import streamlit_authenticator as stauth 
#pip install streamlit-authenticator==0.1.5 
import duckdb
import pickle
from pathlib import Path
import pandas as pd
import logging

from core.duckdb_connector import *
#from duckdb_connector import *

from core.utils import handle_exception
#from utils import handle_exception
logging.basicConfig(level=logging.INFO)
import yaml
from yaml.loader import SafeLoader
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
class Authenticator:
    def __init__(self) -> None:
        self.conn = DuckdbConnector()

    logging.info("----------- Running log_in()-----------")
    @handle_exception(has_random_message_printed_out=True)
    def log_in(self):
        "return yes, no and none for auth status"
        #self.conn.create_users_table()
        users = self.conn.fetch_users()
        #print("og config________",config['credentials'])
        #print(users)
        config['credentials']['usernames']={}
        #{'usernames': {'tu': {'email': 'tu@gmail.com', 'logged_in': False, 'name': 'Thi Minh Tu', 'password': 'Protein'}, 'tyler': {'email': 'nyan@gmail.com', 'logged_in': False, 'name': 'Nyan Htun', 'password': 'Vitamin A'}}}
        for username, (username, user_id, password) in enumerate(users):
            config['credentials']['usernames'][username] = {'email': user_id,'logged_in': False, 'name': username, 'password':password}
        #print("------------My-------------",config['credentials'])
        self.authenticator = stauth.Authenticate(config['credentials'],'cookie','abcdefqwe',0,{'emails': ['@uts.edu.au']})
        self.name, self.authentication_status, self.username = self.authenticator.login()
        return self.name, self.authentication_status, self.username
    def log_out(self):
        if st.session_state["authentication_status"]:
            self.authenticator.logout()
            st.write(f'Welcome *{st.session_state["name"]}*')
            st.write('Some content')
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
    @handle_exception(has_random_message_printed_out=True)
    def register_user_form(self):
        with st.form("sign_up_form"):
            st.write("Register new user")
            user_id = st.text_input('User Id / Email')
            username = st.text_input('Username')
            slider_age = st.slider("Age slider")
            gender_option = st.selectbox('How would you describe your gender?',
                            ('Male', 'Female', 'Other'))
            password = st.text_input('Password',type='password')
            re_password = st.text_input('Repeat password',type='password')
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                if password==re_password:
                    st.write("age", slider_age, "userID", user_id, 'username',username,'password',password)
                    new_user_df = {"user_id": user_id,
                                "gender": gender_option,
                                "age": slider_age,
                                "username": username,
                                "password": password
                                }   
                    self.conn.insert_user(new_user_df)
            st.write("Outside the form",self.conn.fetch_users)

#
#auth = Authenticator()
#auth.log_in()
#auth.register_user()


"""if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password') """
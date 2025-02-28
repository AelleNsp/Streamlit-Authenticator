import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit.components.v1 as components

from .hasher import Hasher
from .authenticate import Authenticate

_RELEASE = True

if not _RELEASE:
    # Loading config file
    with open('../config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Creating the authenticator object
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'], 
        config['cookie']['key'], 
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Creating a login widget
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)
        
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Creating a password reset widget
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

    # Creating a new user registration widget
    try:
        email_register_user, username_register_user, name_register_user = authenticator.register_user(preauthorization=False)
        if email_register_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

    # Creating a forgot password widget
    try:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password()
        if username_forgot_pw:
            st.success('New password sent securely')
            # Random password to be transferred to the user securely
        else:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

    # Creating a forgot username widget
    try:
        username_forgot_username, email_forgot_username = authenticator.forgot_username()
        if username_forgot_username:
            st.success('Username sent securely')
            # Username to be transferred to the user securely
        else:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

    # Creating an update user details widget
    if st.session_state["authentication_status"]:
        try:
            if authenticator.update_user_details(st.session_state["username"]):
                st.success('Entries updated successfully')
        except Exception as e:
            st.error(e)

    # Saving config file
    with open('../config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
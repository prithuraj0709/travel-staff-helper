import streamlit as st
import google.generativeai as genai
import os

# 1. CONFIGURATION
st.set_page_config(page_title="Travel Assistant", page_icon="✈️")
st.title("Internal Staff Assistant")
st.write("Ask questions about SOPs, Sustainability, or Operations.")

# 2. SETUP API KEY (This pulls from the "Secrets" we will set later)
my_api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=my_api_key)

# 3. CHAT INTERFACE
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

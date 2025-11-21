import streamlit as st
import google.generativeai as genai
import pandas as pd

# ---------------------------------------------------------
# CONFIGURATION & SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Hotel Rate Checker", page_icon="🏨")
st.title("Hotel Rate Reference Tool")

# 1. LOAD THE CSV DATA
try:
    # This reads your uploaded file
    df = pd.read_csv("Hotel Rates.csv")
    # This converts the data into a text format the AI can read
    data_for_ai = df.to_markdown(index=False)
except FileNotFoundError:
    st.error("🚨 Error: Could not find 'rates.csv'. Please upload it to GitHub.")
    st.stop()

# 2. CONFIGURE THE AI BRAIN
system_instructions = f"""
You are an expert Hotel Rate Assistant for internal staff.

YOUR INSTRUCTIONS:
1. Use the DATA provided below to answer questions.
2. If the hotel is not in the list, state: "Rate not found in current database."
3. Always mention the validity dates and room category.
4. If the user asks for a destination (e.g., "Hotels in Jaipur"), list the options available in the data.

DATA DATABASE:
{data_for_ai}
"""

# 3. CONNECT TO GOOGLE
try:
    my_api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    st.error("API Key not found. Check Streamlit Secrets.")
    st.stop()

genai.configure(api_key=my_api_key)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=system_instructions
)

# ---------------------------------------------------------
# CHAT INTERFACE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask for a hotel rate (e.g., 'Taj Mahal Hotel Delhi')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching database..."):
            try:
                # Send conversation history for context
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": m["content"]}
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

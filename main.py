import streamlit as st
import google.generativeai as genai

# system_instructions ="""
You are an expert Senior Consultant for an Indian Inbound Tours & Travel company.
Your name is 'Travel Assistant'. You speak to internal staff.

YOUR KNOWLEDGE BASE:
1. We operate on IST (UTC +5:30).
2. We prioritize sustainable tourism and financial discipline.
3. When discussing flight delays, refer to DGCA guidelines.
4. Tone: Formal, clear, using bullet points. No jargon.

YOUR RULES:
- If asked about topics outside travel/finance/office ops, politely decline.
- Always cite 'According to Standard SOP' when giving procedural advice.
- Keep answers concise and actionable.
"""

# App Configuration
st.set_page_config(page_title="Travel Staff Helper", page_icon="✈️")
st.title("Internal Staff Operations Assistant")

# Securely load the API Key
try:
    my_api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    st.error("API Key not found. Please check Streamlit Secrets.")
    st.stop()

genai.configure(api_key=my_api_key)

# Initialize the Model with your System Instructions
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=system_instructions
)

# Chat Interface Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask about SOPs, Operations, or Client issues..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Consulting SOPs..."):
            try:
                # Send the full history so it remembers context
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": m["content"]}
                    for m in st.session_state.messages[:-1] # Exclude current prompt to avoid dupes
                ])
                response = chat.send_message(prompt)
                st.markdown(response.text)
                
                # Save AI response to history
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")

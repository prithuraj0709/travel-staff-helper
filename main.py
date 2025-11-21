import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. APP CONFIGURATION
st.set_page_config(page_title="Hotel Rate Checker", page_icon="🏨", layout="wide")
st.title("Hotel Rate Reference Tool")

# 2. LOAD DATA
try:
    df = pd.read_csv("Hotel Rates.csv", encoding="latin1")
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    st.error("🚨 Error: 'Hotel Rates.csv' not found.")
    st.stop()

# 3. FILTERS
try:
    city_list = sorted(df['City Code'].astype(str).unique())
    selected_city = st.selectbox("Step 1: Select City Code", city_list)

    hotels_in_city = df[df['City Code'] == selected_city]

    hotel_list = sorted(hotels_in_city['Hotel'].astype(str).unique())
    selected_hotel = st.selectbox("Step 2: Select Hotel", hotel_list)

    hotel_data = hotels_in_city[hotels_in_city['Hotel'] == selected_hotel]
except KeyError as e:
    st.error(f"🚨 Column Error: {e}")
    st.stop()

# 4. DISPLAY RATES
st.divider()

if not hotel_data.empty:
    st.subheader(f"Rate Details: {selected_hotel}")

    for index, row in hotel_data.iterrows():
        
        # --- THE FIX: NO INDENTATION HERE ---
        # We push the HTML all the way to the left to prevent errors.
        html_card = f"""
<style>
    .rate-table {{ width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 14px; border: 1px solid black; margin-bottom: 20px; background-color: white; }}
    .rate-table td {{ border: 1px solid black; padding: 8px; vertical-align: top; color: black; }}
    .lbl {{ color: #00B0F0; font-weight: bold; display: block; font-size: 12px; margin-bottom: 2px; }}
    .val {{ color: black; font-weight: normal; }}
</style>
<table class="rate-table">
    <tr>
        <td><span class="lbl">City Code</span><span class="val">{row.get('City Code', '-')}</span></td>
        <td><span class="lbl">Hotel</span><span class="val">{row.get('Hotel', '-')}</span></td>
        <td><span class="lbl">Rate</span><span class="val">{row.get('Rate', '-')}</span></td>
        <td><span class="lbl">From</span><span class="val">{row.get('From', '-')}</span></td>
        <td><span class="lbl">To</span><span class="val">{row.get('To', '-')}</span></td>
        <td><span class="lbl">Room</span><span class="val">{row.get('Room', '-')}</span></td>
    </tr>
    <tr>
        <td><span class="lbl">Type</span><span class="val">{row.get('Type', '-')}</span></td>
        <td><span class="lbl">Plan</span><span class="val">{row.get('Plan', '-')}</span></td>
        <td><span class="lbl">Sr Net Cost</span><span class="val">{row.get('Sr Net Cost', '-')}</span></td>
        <td><span class="lbl">Dr Net Cost</span><span class="val">{row.get('Dr Net Cost', '-')}</span></td>
        <td><span class="lbl">Eb Net Cost</span><span class="val">{row.get('Eb Net Cost', '-')}</span></td>
        <td><span class="lbl">Days</span><span class="val">{row.get('Days', '-')}</span></td>
    </tr>
    <tr>
        <td colspan="3" height="50">
            <span class="lbl">Contract Remarks</span>
            <div class="val">{row.get('Contract Remarks', '-')}</div>
        </td>
        <td colspan="3" height="50">
            <span class="lbl">Sp Noting</span>
            <div class="val">{row.get('Sp Noting', '-')}</div>
        </td>
    </tr>
</table>
"""
        # --- END OF FIX ---

        st.markdown(html_card, unsafe_allow_html=True)

else:
    st.warning("No rates found.")

# 5. AI ASSISTANT
st.write("---")
if prompt := st.chat_input("Ask about this hotel..."):
    with st.chat_message("user"):
        st.write(prompt)
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.chat_message("assistant"):
            st.write(model.generate_content(f"Data: {hotel_data.to_markdown()}\nQ: {prompt}").text)

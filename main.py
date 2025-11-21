import streamlit as st
import pandas as pd

# 1. APP CONFIGURATION
st.set_page_config(page_title="Hotel Rates", page_icon="🏨", layout="wide")
st.title("Hotel Rates")

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
        
        # Helper: Format Days (remove .0)
        days_val = str(row.get('Days', '-')).replace('.0', '')
        
        # --- HTML CONSTRUCTION ---
        # Layout: 12 Columns Total
        # Note: The chat section has been removed from the bottom.
        
        html_card = f"""
<style>
    .rate-table {{ width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 13px; border: 1px solid black; margin-bottom: 20px; background-color: white; }}
    .rate-table td {{ border: 1px solid black; padding: 5px; vertical-align: top; color: black; text-align: center; }}
    .lbl {{ color: #00B0F0; font-weight: bold; display: block; font-size: 10px; margin-bottom: 2px; text-transform: uppercase; white-space: nowrap; }}
    .val {{ color: black; font-weight: normal; }}
    .cost-col {{ background-color: #eaf6ff; }}
    .remarks {{ text-align: left; padding: 8px; background-color: #f9f9f9; }}
</style>
<table class="rate-table">
    <tr>
        <td><span class="lbl">City</span><span class="val">{row.get('City Code', '-')}</span></td>
        <td><span class="lbl">Hotel</span><span class="val">{row.get('Hotel', '-')}</span></td>
        <td><span class="lbl">Rate Code</span><span class="val">{row.get('Rate', '-')}</span></td>
        <td><span class="lbl">From</span><span class="val">{row.get('From', '-')}</span></td>
        <td><span class="lbl">To</span><span class="val">{row.get('To', '-')}</span></td>
        <td><span class="lbl">Room</span><span class="val">{row.get('Room', '-')}</span></td>
        <td><span class="lbl">Type</span><span class="val">{row.get('Type', '-')}</span></td>
        
        <td class="cost-col"><span class="lbl">Plan</span><span class="val">{row.get('Plan', '-')}</span></td>
        <td class="cost-col"><span class="lbl">SGL (Sr)</span><span class="val">{row.get('Sr Net Cost', '-')}</span></td>
        <td class="cost-col"><span class="lbl">DBL (Dr)</span><span class="val">{row.get('Dr Net Cost', '-')}</span></td>
        <td class="cost-col"><span class="lbl">E.Bed (Eb)</span><span class="val">{row.get('Eb Net Cost', '-')}</span></td>
        
        <td><span class="lbl">Days</span><span class="val">{days_val}</span></td>
    </tr>
    <tr>
        <td colspan="6" class="remarks"><span class="lbl">Contract Remarks</span><div class="val" style="white-space: pre-wrap;">{row.get('Contract Remarks', '-')}</div></td>
        <td colspan="6" class="remarks"><span class="lbl">Sp Noting</span><div class="val" style="white-space: pre-wrap;">{row.get('Sp Noting', '-')}</div></td>
    </tr>
</table>
""".replace("\n", "") 

        st.markdown(html_card, unsafe_allow_html=True)

else:
    st.warning("No rates found.")

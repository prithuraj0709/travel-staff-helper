import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. APP CONFIGURATION
st.set_page_config(page_title="Hotel Rate Checker", page_icon="🏨")
st.title("Hotel Rate Reference Tool")

# 2. LOAD DATA
try:
    # We use latin1 to handle special currency symbols
    df = pd.read_csv("Hotel Rates.csv", encoding="latin1")
    
    # --- IMPORTANT: CLEAN UP COLUMN NAMES ---
    # This removes extra spaces from headers (e.g., "City " becomes "City")
    df.columns = df.columns.str.strip()
    
except FileNotFoundError:
    st.error("🚨 Error: 'Hotel Rates.csv' not found on GitHub.")
    st.stop()

# 3. CREATE DROPDOWNS (LOVs)
# ---------------------------------------------------------

# A. Create the City Dropdown
# We get unique values from the 'City' column and sort them
try:
    # REPLACE 'City' below with your exact CSV column name if different
    city_list = sorted(df['City Code'].astype(str).unique()) 
    selected_city = st.selectbox("Step 1: Select City / City Code", city_list)

    # B. Filter data based on selected City
    hotels_in_city = df[df['City Code'] == selected_city]

    # C. Create the Hotel Dropdown
    # REPLACE 'Hotel Name' below with your exact CSV column name if different
    hotel_list = sorted(hotels_in_city['Hotel'].astype(str).unique())
    selected_hotel = st.selectbox("Step 2: Select Hotel", hotel_list)

    # D. Get the specific row for that hotel
    hotel_data = hotels_in_city[hotels_in_city['Hotel'] == selected_hotel]

except KeyError as e:
    st.error(f"🚨 Column Name Error: Your CSV does not have a column named {e}. Please check your CSV headers.")
    st.stop()

# 4. DISPLAY THE RATE (Custom Layout)
# ---------------------------------------------------------
st.divider()

if not hotel_data.empty:
    st.subheader(f"Rate Details: {selected_hotel}")
    
    # Loop through rows
    for index, row in hotel_data.iterrows():
        
        # Define the HTML
        html_card = f"""
        <style>
            .rate-table {{
                width: 100%;
                border-collapse: collapse;
                font-family: Arial, sans-serif;
                font-size: 14px;
                border: 1px solid black;
                margin-bottom: 20px;
            }}
            .rate-table td {{
                border: 1px solid black;
                padding: 8px;
                vertical-align: top;
            }}
            .lbl {{
                color: #00B0F0;
                font-weight: bold;
                display: block;
                font-size: 12px;
                margin-bottom: 2px;
            }}
            .val {{
                color: black;
                font-weight: normal;
            }}
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
        
        # RENDER THE HTML (Aligned with html_card above)
        st.markdown(html_card, unsafe_allow_html=True)

else:
    st.warning("No rate details found for this selection.")

# 5. OPTIONAL: ASK AI FOR DETAILS (Hybrid Feature)
# ---------------------------------------------------------
st.write("---")
st.write("💡 **Need more info?** Ask the AI about this specific hotel below:")

# Setup AI
try:
    my_api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=my_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("AI features disabled (API Key missing).")

if prompt := st.chat_input("Ex: Does this rate include breakfast?"):
    # We feed the AI only the specific row user selected
    context = f"""
    You are a helper. Answer the user question based ONLY on this data:
    {hotel_data.to_markdown(index=False)}
    """
    
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        response = model.generate_content(context + "\nUser Question: " + prompt)
        st.write(response.text)

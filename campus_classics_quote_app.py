import math
import streamlit as st
import io
from fpdf import FPDF
from datetime import datetime

# Pricing data and calculation logic
prices = {
    'Comfort Colors Pocket': {'light': (24, 28), 'dark': (26, 30)},
    'Comfort Colors 1717': {'light': (24, 28), 'dark': (25, 29)},
    'Port & Co Pocket (PC54P)': {'light': (22, 25), 'dark': (23, 26)},
    'Port & Co Non-Pocket (PC54)': {'light': (21, 24), 'dark': (22, 25)},
    'Tultex 202': {'light': (19, 22), 'dark': (20, 23)},
    'Gildan': {'light': (16, 22), 'dark': (16, 22)},
    'Nike Polo (NKDC1963)': {'any': (59.95, 64.95)},
    'Adidas Polo (A230)': {'any': (59.95, 64.95)},
    'Port & Co Polo (K110)': {'any': (36.95, 40)},
    'SportTek Polo (ST550)': {'any': (34.95, 36.95)},
    'Sportsman Hat (AH35)': {'any': (23, 25)},
}

heatseal_prices = {
    'left chest': [(24, 0.36), (49, 0.33), (99, 0.30), (249, 0.27), (99999, 0.24)],
    'full back large': [(24, 8.64), (49, 7.92), (99, 7.20), (249, 6.48), (99999, 5.76)],
    'full back small': [(24, 7.20), (49, 6.60), (99, 6.00), (249, 5.40), (99999, 4.80)]
}

placement_fees = {
    'light': {
        'left chest': [2.75, 2.40, 2.05, 1.70],
        'full front/back': [4.25, 4.00, 3.25, 3.50]
    },
    'dark': {
        'left chest': [3.75, 3.40, 3.05, 2.70],
        'full front/back': [6.00, 5.65, 5.30, 4.95]
    }
}

def get_heatseal_cost(placement, quantity):
    if placement == 'left chest':
        table = heatseal_prices['left chest']
    elif placement == 'full back large':
        table = heatseal_prices['full back large']
    else:
        table = heatseal_prices['full back small']
    for max_qty, price in table:
        if quantity <= max_qty:
            return price

# Streamlit web app
st.title("Campus Classics Quick Quote Calculator")

with st.form(key='quote_form'):
    customer_name = st.text_input('Customer Name')
    event_name = st.text_input('Event Name')
    garment = st.selectbox('Select Garment Type', list(prices.keys()))
    color = st.selectbox('Select Garment Color', ['light', 'dark'])
    quantity = st.number_input('Enter Quantity', min_value=1, value=24)
    is_heatseal = st.radio('Use Heatseal for Front?', ['No', 'Yes'])

    if is_heatseal == 'No':
        decoration = st.selectbox('Decoration Method', ['screenprint', 'dtg', 'embroidery'])
    else:
        decoration = 'heatseal'

    if 'Hat' in garment:
        placement = st.selectbox('Placement', ['front'])
    else:
        placement = st.selectbox('Placement', ['left chest', 'full front large', 'full back small'])

    submit_button = st.form_submit_button(label='Calculate Quote')

if submit_button:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    color_key = 'any' if 'any' in prices[garment] else ('dark' if color.lower() == 'dark' else 'light')
    price_range = prices[garment][color_key]

    if quantity < 25:
        base_price = price_range[1]
    elif quantity < 51:
        base_price = (price_range[0] + price_range[1]) / 2
    elif quantity < 145:
        base_price = price_range[0] * 0.95
    else:
        base_price = price_range[0] * 0.90

    if is_heatseal == 'Yes':
        add_cost = get_heatseal_cost(placement if placement != 'front' else 'left chest', quantity)
    else:
        placement_key = 'full front/back' if 'full' in placement else 'left chest'
        if quantity < 25:
            add_cost = placement_fees[color_key][placement_key][0]
        elif quantity < 51:
            add_cost = placement_fees[color_key][placement_key][1]
        elif quantity < 145:
            add_cost = placement_fees[color_key][placement_key][2]
        else:
            add_cost = placement_fees[color_key][placement_key][3]

    final_price = round(base_price + add_cost, 2)

    st.success(f"Quick quote: ${final_price} per item")

    clean_customer = customer_name.strip().replace(" ", "_").replace("/", "_")
    clean_event = event_name.strip().replace(" ", "_").replace("/", "_")
    file_prefix = f"{clean_customer}_{clean_event}" if clean_customer and clean_event else "campus_classics_quote"

    summary = f"""
    Customer Name: {customer_name}
    Event Name: {event_name}
    Garment: {garment}
    Color: {color.title()}
    Quantity: {quantity}
    Decoration Method: {decoration.title()}
    Placement: {placement.title()}
    Final Price Per Item: ${final_price}
    Date: {now}
    """

    buffer = io.StringIO()
    buffer.write(summary)
    buffer.seek(0)

    st.download_button(
        label="Download Quote as Text File",
        data=buffer.getvalue(),
        file_name=f"{file_prefix}.txt",
        mime="text/plain"
    )

    class PDF(FPDF):
        def header(self):
            try:
                self.image('logo.png', x=80, y=8, w=50)
            except:
                pass
            self.ln(35)
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, 'Campus Classics Quote Summary', ln=True, align='C')
            self.ln(10)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'Campus Classics - www.campusclassics.com', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(summary)

    pdf_bytes = pdf.output(dest='S').encode('latin1', 'replace')

    st.download_button(
        label="Download Quote as PDF",
        data=pdf_bytes,
        file_name=f"{file_prefix}.pdf",
        mime="application/pdf"
    )

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

embroidery_pricing = [
    (2000, [7.75, 3.91, 3.45, 3.06, 2.88, 2.41]),
    (4000, [9.08, 5.11, 4.37, 3.45, 3.22, 2.76]),
    (6000, [9.95, 5.87, 4.95, 4.03, 3.57, 3.22]),
    (8000, [10.29, 6.32, 5.29, 4.37, 4.03, 3.57]),
    (10000, [10.93, 6.90, 5.87, 4.89, 4.60, 4.03]),
    (12000, [11.50, 7.89, 6.32, 5.40, 4.95, 4.30]),
]

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

def calculate_custom_price(garment_type, color, quantity, decoration_method, placement='left chest', stitch_count=0, extra_ink_cc=0):
    color_key = 'any' if 'any' in prices[garment_type] else ('dark' if color.lower() == 'dark' else 'light')
    price_range = prices[garment_type][color_key]

    if quantity < 25:
        base_price = price_range[1]
    elif quantity < 51:
        base_price = (price_range[0] + price_range[1]) / 2
    elif quantity < 145:
        base_price = price_range[0] * 0.95
    else:
        base_price = price_range[0] * 0.90

    final_price = base_price

    if decoration_method.lower() == 'embroidery':
        stitch_bracket = next((pricing for limit, pricing in embroidery_pricing if stitch_count <= limit), embroidery_pricing[-1][1])
        if quantity < 6:
            embroidery_cost = stitch_bracket[0]
        elif quantity < 25:
            embroidery_cost = stitch_bracket[1]
        elif quantity < 73:
            embroidery_cost = stitch_bracket[2]
        elif quantity < 145:
            embroidery_cost = stitch_bracket[3]
        elif quantity < 289:
            embroidery_cost = stitch_bracket[4]
        else:
            embroidery_cost = stitch_bracket[5]
        final_price += embroidery_cost

    elif decoration_method.lower() in ['screenprint', 'dtg']:
        placement_options = placement_fees[color_key]
        placement_cost = placement_options[placement.lower()][0] if quantity < 25 else placement_options[placement.lower()][1] if quantity < 51 else placement_options[placement.lower()][2] if quantity < 145 else placement_options[placement.lower()][3]
        ink_surcharge = max(0, extra_ink_cc - 7) * 1.0 if color_key == 'dark' else 0
        final_price += placement_cost + ink_surcharge

    return round(final_price, 2)

# Streamlit web app
st.title("Campus Classics Quick Quote Calculator")

with st.form(key='quote_form'):
    customer_name = st.text_input('Customer Name')
    event_name = st.text_input('Event Name')
    garment = st.selectbox('Select Garment Type', list(prices.keys()))
    color = st.selectbox('Select Garment Color', ['light', 'dark'])
    quantity = st.number_input('Enter Quantity', min_value=1, value=24)
    decoration = st.selectbox('Decoration Method', ['screenprint', 'dtg', 'embroidery'])
    placement = st.selectbox('Placement (for screenprint/DTG)', ['left chest', 'full front/back'])
    stitch_count = st.number_input('Stitch Count (for embroidery)', min_value=0, value=0)
    extra_ink_cc = st.number_input('Extra Ink CCs over 7 (for DTG)', min_value=0, value=0)
    submit_button = st.form_submit_button(label='Calculate Quote')

if submit_button:
    quote = calculate_custom_price(garment, color, quantity, decoration, placement, stitch_count, extra_ink_cc)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    st.success(f"Quick quote: ${quote} per item")

    summary = f"""
    Campus Classics Quote Summary
    -----------------------------
    Date: {now}
    Customer Name: {customer_name}
    Event Name: {event_name}
    Garment: {garment}
    Color: {color.title()}
    Quantity: {quantity}
    Decoration Method: {decoration.title()}
    Placement: {placement.title()}
    Stitch Count: {stitch_count} (if embroidery)
    Extra Ink CCs: {extra_ink_cc} (if DTG)
    Final Price Per Item: ${quote}
    """

    st.text_area("Quote Summary", summary, height=250)

    clean_customer = customer_name.strip().replace(" ", "_").replace("/", "_")
    clean_event = event_name.strip().replace(" ", "_").replace("/", "_")
    file_prefix = f"{clean_customer}_{clean_event}" if clean_customer and clean_event else "campus_classics_quote"

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
            self.ln(20)
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Campus Classics Quote Summary', ln=True, align='C')
            self.ln(10)

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, ln=True, align='L')
            self.ln(5)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'Campus Classics - www.campusclassics.com', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Quote Details')
    pdf.chapter_body(summary)

    pdf_bytes = pdf.output(dest='S').encode('latin1', 'replace')

    st.download_button(
        label="Download Quote as PDF",
        data=pdf_bytes,
        file_name=f"{file_prefix}.pdf",
        mime="application/pdf"
    )

import math
import streamlit as st
import io
from fpdf import FPDF
from datetime import datetime

# (All previous definitions remain unchanged)

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

    st.markdown(f"""
    ### 📋 Quote Summary
    - **Customer Name**: {customer_name}
    - **Event Name**: {event_name}
    - **Garment**: {garment}
    - **Color**: {color.title()}
    - **Quantity**: {quantity}
    - **Decoration Method**: {decoration.title()}
    - **Placement**: {placement.title()}
    - **Stitch Count**: {stitch_count} (if embroidery)
    - **Extra Ink CCs**: {extra_ink_cc} (if DTG)
    - **Final Price Per Item**: **${quote}**
    - **Date/Time**: {now}
    """)

    # Sanitize file names
    clean_customer = customer_name.strip().replace(" ", "_").replace("/", "_")
    clean_event = event_name.strip().replace(" ", "_").replace("/", "_")
    file_prefix = f"{clean_customer}_{clean_event}" if clean_customer and clean_event else "campus_classics_quote"

    buffer = io.StringIO()
    buffer.write(summary)
    buffer.seek(0)
    st.download_button(
        label="Download Quote as Text File",
        data=buffer,
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
            self.cell(0, 10, 'Campus Classics • www.campusclassics.com', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title('Quote Details')
    pdf.chapter_body(summary)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_bytes)

    st.download_button(
        label="Download Quote as PDF",
        data=pdf_buffer,
        file_name=f"{file_prefix}.pdf",
        mime="application/pdf"
    )

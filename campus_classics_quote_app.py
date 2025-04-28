import math
import streamlit as st

# Pricing dictionaries moved OUTSIDE the function
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
        'full front/back': [4.25, 4.00, 2.75, 3.50]
    },
    'dark': {
        'left chest': [3.75, 3.40, 3.05, 2.70],
        'full front/back': [6.00, 5.65, 5.30, 4.95]
    }
}

def calculate_custom_price(garment_type, color, quantity, decoration_method, placement='left chest', stitch_count=0, extra_ink_cc=0):
    # FUNCTION stays the same, just remove those dictionary definitions inside it
    ...

# Now Streamlit can properly access 'prices'
st.title("Campus Classics Quick Quote Calculator")

garment = st.selectbox('Select Garment Type', list(prices

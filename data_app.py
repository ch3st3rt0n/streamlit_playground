# Imports
import streamlit as st
from pathlib import Path
import pandas as pd
import re


def get_dataset_path():
    return Path('data/customer_reviews.csv')

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r'^\s\w', '', text)
    return text

# Set up the streamlit interface
st.title("Customer reviews application.")
st.write("Experiment with data processing by Gen AI.")

# Define the layout
col1, col2 = st.columns(2)

with col1:
    if st.button('Ingest Dataset'):
        try:
            st.session_state['df'] = pd.read_csv(get_dataset_path())
            st.success('Data Ingested Successfully.')
        except FileNotFoundError:
            st.error('Data file not found.')

with col2:
    if st.button('Parse Reviews'):
        if 'df' in st.session_state:
            st.session_state['df']['CLEANED_SUMMARY'] = st.session_state['df']['SUMMARY'].apply(clean_text)

        else:
            st.warning('Please ingest the dataset first.')


# Display if dataset is ingested
if 'df' in st.session_state:
    st.subheader('Product Filter')
    product = st.selectbox('Choose a product', ['All'] + list(st.session_state['df']['PRODUCT'].unique()))
    st.subheader('Dataset Preview')

    # Filter the dataframe by product
    if product == 'All':
        df_display = st.session_state['df']
    else:
        df_display = st.session_state['df'][st.session_state['df']['PRODUCT'] == product]
    st.dataframe(df_display)

    # Add sentiment score bar chart
    st.subheader('Average sentiment scores by Product')
    chart_data = st.session_state['df'].groupby('PRODUCT')['SENTIMENT_SCORE'].mean()
    st.bar_chart(chart_data)

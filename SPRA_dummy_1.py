import os
import pandas as pd
import streamlit as st
from fuzzywuzzy import fuzz
import io
import base64

# Function to perform fuzzy matching
def fuzzy_match(val1, list1, threshold=96):
    val1 = str(val1)
    list1 = list(map(str, list1))

    best_matched_value = None
    max_score = threshold

    for item in list1:
        score = fuzz.token_set_ratio(val1, str(item))
        if score >= threshold and score > max_score:
            max_score = score
            best_matched_value = item

    return best_matched_value if max_score >= threshold else None

# Define the Streamlit app
def main():
    # Set the app title
    st.title("SPRA Dummy")

    # Add a subheading for document processing
    st.subheader("Upload Documents for Fuzzy Match")

    # Upload BOM, QnC, and OTIF Excel files
    bom_file = st.file_uploader("Upload BOM Excel File", type=["xlsx"])
    qnc_file = st.file_uploader("Upload QnC Excel File", type=["xlsx"])
    otif_file = st.file_uploader("Upload OTIF Excel File", type=["xlsx"])

    # Check if files are uploaded
    if bom_file and qnc_file and otif_file:
        # Read the uploaded Excel files
        bom_df = pd.read_excel(bom_file)
        qnc_df = pd.read_excel(qnc_file)
        otif_df = pd.read_excel(otif_file)

        # Extract specific columns from BOM, QnC, and OTIF files
        bom_column1 = bom_df['BOM Supplier Name and City']
        bom_column2 = bom_df['BOM Supplier Name']
        qnc_column = qnc_df['QnC Cleaned Supplier Name']
        otif_column = otif_df['OTIF Supplier Name']

        # Create master data
        master_data = pd.DataFrame()
        master_data['BOM Supplier Name and City'] = bom_column1
        master_data['QnC Cleaned Supplier Name'] = qnc_column
        master_data['BOM Supplier Name'] = bom_column2
        master_data['OTIF Supplier Name'] = otif_column

        # Perform fuzzy matching for QnC and OTIF
        master_data['Matched QnC Supplier Name'] = master_data['BOM Supplier Name and City'].apply(
            lambda x: fuzzy_match(x, qnc_column.dropna().unique())
        )
        master_data['Matched OTIF Supplier Name'] = master_data['BOM Supplier Name'].apply(
            lambda x: fuzzy_match(x, otif_column.dropna().unique())
        )

        # Display the output data in the app
        st.subheader("Output Data")
        
        st.write(master_data)

if __name__ == '__main__':
    main()

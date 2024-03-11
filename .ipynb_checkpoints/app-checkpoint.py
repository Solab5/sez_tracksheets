import streamlit as st
import pandas as pd
from collections import defaultdict
from io import BytesIO
import os

# Function to assign status
def assign_status(group, targets, reserves):
    count = defaultdict(int)
    status = []

    for idx, row in group.iterrows():
        cat = row['HHHeadship']
        
        if cat not in targets or cat not in reserves:
            status.append('unknown')
            continue

        count[cat] += 1

        if count[cat] <= targets[cat]:
            status.append('target')
        elif count[cat] <= targets[cat] + reserves[cat]:
            status.append('reserve')
        else:
            status.append('exceed')

    group['status'] = status
    return group

# Streamlit app
st.title('RTV Standard Evaluations Status Assignment')

# Upload the Excel file
file = st.file_uploader('Upload an excel file', type=['xls', 'xlsx'])

if file:
    data = pd.read_excel(file)
    st.write("Preview of Data")
    st.write(data.head())

    # Assign default targets and reserves (Modify as needed)
    targets = {'Male Headed': 9, 'Female Headed': 3, 'Youth Headed': 3}
    reserves = {'Male Headed': 5, 'Female Headed': 2, 'Youth Headed': 2}

    # Process the data
    df = data.groupby('village', group_keys=False).apply(assign_status, targets=targets, reserves=reserves)
    st.write("Processed Data")
    st.write(df.head())

    # Download the processed DataFrame
    #st.download_button('Download Processed Data', df.to_csv(index=False), file_name='processed_data.csv')


# Option to save the final file
    if st.button("Download File"):
    # Convert the sampled data to an Excel file
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        # Create a button to download the Excel file
        st.download_button(
            label="Download File as Excel",
            data=excel_file.getvalue(),
            file_name=f"tracksheet.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

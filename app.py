import streamlit as st

from script import compute_progress

st.title('Compute Progress ')
f1 = st.file_uploader('CSV Extracted TFS')
if f1:
    compute_progress(f1, "out.xlsx")
    with open("out.xlsx", "rb") as file:
        st.download_button("Download Excel", data=file,
                           file_name="progress.xlsx")

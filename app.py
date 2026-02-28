import streamlit as st
from src.engine import process_risk_data
from src.visualizations import get_pillar_chart, get_risk_bar
import zipfile
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="Risk Analyzer", layout="wide")

st.title("Risk Analysis Graph Dashboard")

uploaded_file = st.file_uploader("Upload 'Analysis.xlsx'", type="xlsx")

if uploaded_file:
    # 1. Run Engine
    data_avg, averages_df, ids = process_risk_data(uploaded_file)
    
    # 2. Sidebar Selection
    supplier_list = data_avg['SUPPLIER'].tolist()
    selected_supplier = st.sidebar.selectbox("Select a Supplier to Inspect", supplier_list)
    
    # 3. Get specific row
    row_data = data_avg[data_avg['SUPPLIER'] == selected_supplier].iloc[0]
    
    # 4. Display Graphs
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_pillars = get_pillar_chart(row_data, averages_df)
        st.pyplot(fig_pillars)
        
    with col2:
        fig_risk = get_risk_bar(row_data, averages_df['Risk Rating '].iloc[0])
        st.pyplot(fig_risk)
        st.metric("Risk Score", f"{row_data['Risk Rating ']:.2f}")

    # 5. Download 
    if st.button("Prepare All Reports for Download"):
        zip_buffer = io.BytesIO()
        st.write("Generating ZIP... this might take a second.")
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for index, row in data_avg.iterrows():
                supplier_name = row["SUPPLIER"]
                
                # Generate Pillar Chart
                fig_p = get_pillar_chart(row, averages_df)
                buf_p = io.BytesIO()
                fig_p.savefig(buf_p, format="png")
                zip_file.writestr(f"Pillars_{supplier_name}.png", buf_p.getvalue())
                
                # Generate Risk Bar
                fig_r = get_risk_bar(row, averages_df['Risk Rating '].iloc[0])
                buf_r = io.BytesIO()
                fig_r.savefig(buf_r, format="png")
                zip_file.writestr(f"Risk_{supplier_name}.png", buf_r.getvalue())
                
                # Close figures to save memory
                plt.close(fig_p)
                plt.close(fig_r)

        st.download_button(
            label="Download ZIP",
            data=zip_buffer.getvalue(),
            file_name="Risk_Analysis_Reports.zip",
            mime="application/zip"
        )
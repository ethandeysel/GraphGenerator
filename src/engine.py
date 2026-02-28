import pandas as pd
import numpy as np

def process_risk_data(uploaded_file):
    # Load data
    data = pd.read_excel(uploaded_file, sheet_name='RESULTS', index_col=0, header=1)
    data = np.round(data, 1)
    
    # Clean data
    data_avg = data[data.iloc[:, 5].notna()].copy()

    # Define columns
    ids = ['Risk Rating ', 'A. Context of the Organisation', 'B. Governance & Accountability',
           'C. Cybersecurity Strategy and Framework', 'D. Protection and Prevention',
           'E. Monitoring and Detection', 'F. Incident Response and Recovery', 'G. Independent Reviews']
    
    # Calculate Averages
    col_averages = data_avg[ids].mean()
    averages_df = pd.DataFrame(col_averages).T
    averages_df = np.round(averages_df, 2)
    
    return data_avg, averages_df, ids
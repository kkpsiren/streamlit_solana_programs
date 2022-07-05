import streamlit as st
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
from plots import *


cm = sns.light_palette("green", as_cmap=True)

def landing_page(df, labels):
    
    
    l1,l2 = st.columns((800,300))
    with l2:
        st.image('solana.logo.png',width=300)
    with l1:
        st.markdown("""
# Flipside Crypto <3 Solana
""")
        st.markdown(f"""
## Unique Solana Programs
      
### Intro

Q92. One way to track developer growth in an ecosystem is through the number of unique contracts used. Create a visualization of the number of unique programs used per day since the beginning of January. What type of programs are the most popular, and what programs seem to be gaining in popularity over that timeframe? Does it appear that development is still ongoing in the bear market?
""")

    fig = plot_total_counts(df)
    st.plotly_chart(fig, use_container_width=True)

    
    l0,l1 = st.columns(2)
    fig = piechart(df, n=20)
    with l0:
        st.plotly_chart(fig, use_container_width=True)
    
    fig = do_treemap(df,labels)
    with l1:
        st.plotly_chart(fig, use_container_width=True)
    
    
    plot_data = df.groupby('PROGRAM_ID')['COUNTS'].sum().to_frame().reset_index()
    plot_data = plot_data.merge(labels,left_on='PROGRAM_ID',right_on='ADDRESS',how='left')
    
    l0,l1 = st.columns(2)
    l2,l3 = st.columns(2)
    for i, col in enumerate(['ADDRESS_NAME', 'LABEL','LABEL_TYPE', 'LABEL_SUBTYPE']):
        fig = piechart(plot_data, n=20, col=col)
        with eval(f'l{i}'):
            st.plotly_chart(fig, use_container_width=True)

    col = st.selectbox('Select', ('ADDRESS_NAME','LABEL','LABEL_TYPE','LABEL_SUBTYPE'),index=3)
    options = labels[col].unique()
    selected_options = st.multiselect('Select Items', options, default=options)
    
    filter_df = labels[labels[col].isin(selected_options)].merge(df,left_on='ADDRESS',right_on='PROGRAM_ID',how='inner')
    fig = plot_total_counts(filter_df,col)
    st.plotly_chart(fig, use_container_width=True)

    
    st.markdown(f"""
## Summary
- DEX activity lead by Serum is the most used Program
- Additionally Mango Markets, Jupiter and Saber are gaining popularity
- Orca gained hugely in popularity but has had a quiet July so far.

- Solana's general contracts also see a big activity
- The Worst slump in market activity is down and the market seems to be picking up again from the bear market
  - This is very evident by looking at the moving averages are on the rise again
  - We are still 20 - 33% behind February activity of on average 25M
- **Disclaimer** This data heavily relies on the labeled data from Flipside, hence as not all addresses can be labeled, conclusions should be taken with a grain of salt
- NFT activity and DeFi activity (Solend and Solfarm) seem to have a minor role in the total activity
  
## Methods
For this dashboard used the ShroomDK for querying the data from Flipside. 
But since the Solana Blockchain is filled with transactions, 
we had to split this into separate monthly queries. 
Since the first 6 months of 2022 should not change given the data is complete, we are loading those from 
a hdf-file and we only query the data since the first 6 months. 
We also query the labels based on the addresses we get, although we restrict the data when querying by doing inner joins,
since the label types would stay regardless unknown.
 
Plotly and Pandas are used for the data viz and the app runs with streamlit.


Transaction Query for ProgramIDs:
```
select block_timestamp::date as date, fe.program_id, 
count(distinct(tx_id)) as counts
from solana.core.fact_events fe
inner join solana.core.dim_labels dl on fe.program_id = dl.address
where date_trunc('month',block_timestamp) = '2022-<MONTH-HERE>-01'
and succeeded=TRUE
group by 1,2
```

Label Query:
```
select
address,
address_name,
label,
label_type,
label_subtype
from solana.core.dim_labels
where address in (<LIST OF ADDRESSES FOUND>)
```
                """)

    
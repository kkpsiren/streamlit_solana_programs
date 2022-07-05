def return_query(month):
    if month <10:
        month = f'0{str(month)}'
    elif month in (10,11,12):
        month = str(month)
    else:
        raise AssertionError
    return f"""
  select block_timestamp::date as date, fe.program_id, 
  count(distinct(tx_id)) as counts
  from solana.core.fact_events fe
  inner join solana.core.dim_labels dl on fe.program_id = dl.address
  where date_trunc('month',block_timestamp) = '2022-{month}-01'
  and succeeded=TRUE
  group by 1,2
"""

def get_labels(df):
    labels = df['PROGRAM_ID'].unique()

    labels = [f"'{i}'" for i in labels]

    string = ",".join(labels)

    LABEL_QUERY = f"""
    select
    address,
    address_name,
    label,
    label_type,
    label_subtype
    from solana.core.dim_labels
    where address in ({string})
    """
    return LABEL_QUERY
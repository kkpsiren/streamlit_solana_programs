import plotly.express as px
import plotly.graph_objects as go

def get_ma(data, window=10):
    data2 = data.sort_values('DATE').rolling(window=window)['COUNTS'].mean().reset_index()
    data2['DATE'] = data.sort_values('DATE')['DATE']
    return data2

def plot_total_counts(df, col=None):
    if col is None:
        title='Total Transaction Counts'
    else:
        title=f'{col} Transactions Counts'
    
    if col is None:
        data = df.groupby('DATE')['COUNTS'].sum().to_frame('COUNTS').reset_index()
    else:
        data = df.groupby(['DATE',col])['COUNTS'].sum().to_frame('COUNTS').reset_index()
        
    fig = px.bar(data_frame=data,
        x='DATE',
        y='COUNTS', 
        title = title,
        color=col
                )
    if col is None:
        for i in [10,20,50]:
            data2 = get_ma(data.groupby('DATE')['COUNTS'].sum().to_frame('COUNTS').reset_index(), window=i)
            fig.add_traces(go.Scatter(x= data2['DATE'].tolist(), y=data2['COUNTS'].tolist(), mode = 'lines', name=f'{i}-day MA'))

    return fig

def piechart(df, n=20, col='PROGRAM_ID'):
    ext = 'Program IDs' if col == 'PROGRAM_ID' else f'{" ".join(col.capitalize().split("_"))}s'
    plot_data = df.groupby(col)['COUNTS'].sum().to_frame().reset_index()
    min_value = plot_data.sort_values('COUNTS',ascending=False).head(n)['COUNTS'].min()
    plot_data.loc[plot_data['COUNTS'] < min_value, col] = f'Other {ext}' # Represent only large countries
    if plot_data.shape[0] != n:
        n=''
    fig = px.pie(plot_data, 
                 values='COUNTS', 
                 names=col, title=f'{n} Top {ext}',
                )
    fig.update_traces(textposition='inside', textinfo='percent+value')
    return fig

def do_treemap(df,labels):
    plot_data = df.groupby('PROGRAM_ID')['COUNTS'].sum().to_frame().reset_index()
    plot_data = plot_data.merge(labels,left_on='PROGRAM_ID',right_on='ADDRESS',how='left')

    fig = px.treemap(plot_data, path=['LABEL_TYPE', 'LABEL_SUBTYPE', 'LABEL'], values='COUNTS',
                     title='Treemap based on labels')
    return fig
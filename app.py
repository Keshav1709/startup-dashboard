import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')
df = pd.read_csv('startups_clean.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
    #total invested amount
    total = round(df['amount'].sum())
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head().values[0]
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    num_startup = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + 'USD')
    with col2:
        st.metric('Max', str(max_funding) + 'USD')
    with col3:
        st.metric('average funding', str(round(avg_funding)) + 'USD')
    with col4:
        st.metric('total startups funded', str(num_startup) + 'USD')

    st.header('MOM graph')
    selected_option= st.selectbox('Select Type',['Total','Count'])
    if selected_option =='Total':
        temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis']=temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])

    st.pyplot(fig3)


def load_investor_details(investors):
    st.title(investors)
    #load the recent 5 investments of the investor
    last5_df = df[df['investor'].str.contains(investors)].head()[['date','startup','vertical','city','investor','round','amount']]
    st.subheader('Most recent investments')
    st.dataframe(last5_df)
    col1 , col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series=df[df['investor'].str.contains(investors)].groupby('startup')['amount'].sum().sort_values(ascending=False)
        st.subheader('Biggest investments')
        fig , ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investor'].str.contains(investors)].groupby('vertical')['amount'].sum()
        st.subheader('sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f')

        st.pyplot(fig1)

    df['year']= df['date'].dt.year
    year_series = df[df['investor'].str.contains(investors)].groupby('year')['amount'].sum()
    st.subheader('YOY investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)

    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analaysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option =='Overall Analysis':
        load_overall_analysis()

elif option =='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    st.title('Startup Analysis')
    btn1=st.sidebar.button('Find startup details')
else:
    selected_investor = st.sidebar.selectbox('Select inestor',sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors details')
    if btn2:
        load_investor_details(selected_investor)

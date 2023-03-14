import numpy as np
import yfinance
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_plotly

import Scrappers
import streamlit as st


def generate_analisys(data):
    data_prophet = data.reset_index()
    data_prophet = data_prophet[['Date', "Close"]]
    data_prophet = data_prophet.rename(columns={
        "Date": "ds",
        "Close": "y"
    })
    data_prophet.ds = data_prophet.ds.dt.tz_localize(None)

    model = Prophet(
        interval_width=0.95,
        daily_seasonality=True,
        yearly_seasonality=True,
        weekly_seasonality=True,
    )

    model.fit(data_prophet)

    future_dates = model.make_future_dataframe(periods=90, freq='D')
    forecast = model.predict(future_dates)
    forecast_fig = plot_plotly(model, forecast, xlabel="período", ylabel="valor", figsize=(500, 400))
    st.plotly_chart(forecast_fig)


trendind = Scrappers.get_trending_tickers()
options = [t[0] for t in trendind]

default_ticker = "Select a Ticker"
options.insert(0, default_ticker)
options = np.array(options)

with st.sidebar:
    with st.columns([1, 10, 1])[1]:
        st.image('ProjectLogo.png')
        st.markdown("<h1 style='text-align: center;'>Prophet(Y!Finance)</h1>", unsafe_allow_html=True)
    st.subheader('Enter the Ticker name in the input or select one of the hottest stocks on **Y!Finances**')

    trending_ticker = st.selectbox(
        'Trending Tickers',
        options
    )
    ticker_placeholder = st.empty()
    if trending_ticker:
        personal_ticker = ticker_placeholder.text_input(
            "Ticker ID 👇",
            trending_ticker,
            placeholder='Ticker',
        )

if personal_ticker:
    try:
        data = yfinance.Ticker(personal_ticker)
        if personal_ticker == default_ticker:
            st.markdown(f'<h1>{"Select a Ticker"}</h1>', unsafe_allow_html=True)
        elif data.history().empty:
            st.markdown(f'<h1>O Ticker <u style="color:red;">{personal_ticker}</u> não é válido</h1>',
                        unsafe_allow_html=True)
            st.write('Check the name of the Ticker')
        else:
            st.markdown(
                f'<h1>Analysing <a href="https://finance.yahoo.com/quote/{personal_ticker.replace("^", "%5E")}" style="color:red;"><u>{personal_ticker}</u></a></h1>',
                unsafe_allow_html=True)
            years = st.slider('Number of years in history', 1, 50, 2)
            data = data.history(f'{years}y').reset_index()
            (chart_tab, data_tab) = st.tabs(["📈 Chart", "🗃 Data"])
            data_tab.dataframe(data)
            fig = px.line(data, x='Date', y="Close", title=f"{personal_ticker} close values")
            chart_tab.plotly_chart(fig)
            with st.container():
                generate_analisys(data)

            daily_seasonality = st.checkbox('Daily seasonality ')
            weekly_seasonality = st.checkbox('Weekly_seasonality')
            yearly_seasonality = st.checkbox('Yearly_seasonality')

    except Exception as e:
        st.markdown(f'<h1>{"Selecione um ticker"}</h1>', unsafe_allow_html=True)
else:
    st.markdown(f'<h1>{"Selecione um ticker"}</h1>', unsafe_allow_html=True)

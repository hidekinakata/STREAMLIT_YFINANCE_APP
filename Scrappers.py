import numpy as np
from bs4 import BeautifulSoup
import requests
import streamlit as st


@st.cache_data()
def get_trending_tickers():
    html = requests.get("https://finance.yahoo.com/trending-tickers").content

    soup = BeautifulSoup(html, 'html.parser')

    quotes = soup.select("a[data-test='quoteLink']")
    names = soup.select("td[aria-label='Name']")

    return np.array([[q.contents[0], n.contents[0]] for q, n in zip(quotes, names)])

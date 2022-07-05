import streamlit as st
#from scripts.utils import read_flipside
from landing import landing_page
from beautify import flipside_logo, discord_logo
import os


from data_loading import load_queries, load_data
from queries import *


# from dotenv import load_dotenv
# load_dotenv()
st.set_page_config(page_title="Unique Solana Programs", layout="wide")


df = load_data()
labels = load_queries(get_labels(df))

landing_page(df, labels)

flipside_logo(text="🍄 ShroomDK 🍄")
discord_logo(os.getenv('DISCORD_USERNAME'))
flipside_logo()






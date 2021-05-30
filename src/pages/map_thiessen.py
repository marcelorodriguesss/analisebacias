import streamlit as st
from PIL import Image

from src.pages.utils.data import dbobs_names, basins_names

def main():

    basin = st.selectbox('Selecione a bacia:', tuple(basins_names()))

    for obs in dbobs_names():

        img_path = f'./data/thiessen_figs/{obs}/0_{obs}_{basin}.png'

        image = Image.open(img_path)

        st.image(image, caption=obs.upper())

        st.write('----------------------------------------------------')

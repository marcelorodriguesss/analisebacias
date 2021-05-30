import streamlit as st
from PIL import Image

from src.pages.utils.data import dbobs_names, basins_names

def main():

    basin = st.selectbox('Selecione a bacia:', tuple(basins_names()))

    for obs in dbobs_names():

        img_path = f'./data/wavelets/{basin}/{obs}_wavelets_spectra_{basin}_1981-2020.png'

        image = Image.open(img_path)

        st.image(image)

        st.write('----------------------------------------------------')

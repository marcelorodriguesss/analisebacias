import streamlit as st

import src.pages.accum_mon
import src.pages.annual

PAGES = {
    # "Home": src.pages.home,
    # "Raw Data": src.pages.dashboard,
    "Acumulado Anual": src.pages.annual,
    "Acumulado Mensal": src.pages.accum_mon,
    # "Contribute": src.pages.contribute
}

def main():
    st.sidebar.title("Menu")
    choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
    PAGES[choice].main()
    # st.sidebar.title("About")
    # st.sidebar.info(
    #     """
    #     This app is maintained by Sayar Banerjee. You can learn more about me at
    #     [sayar1106.github.io](https://sayar1106.github.io).
    #     """
    # )
    # st.sidebar.title("Contribute")
    # st.sidebar.info("Feel free to contribute to this open source project. The github link can be found "
    #                 "[here](https://github.com/Sayar1106/covid-dashboard)")

if __name__ == "__main__":
    main()

# from vega_datasets import data

# source = data.stocks()

# st.write(source)

# USAR:
# df['date'] = pd.date_range('2000-1-1', periods=200, freq='D')



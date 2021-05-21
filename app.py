import streamlit as st

import src.pages.accum_mon
import src.pages.annual
import src.pages.map
import src.pages.taylor

PAGES = {
    # "Home": src.pages.home,
    # "Raw Data": src.pages.dashboard,
    "Taylor Diagram": src.pages.taylor,
    "Basins Total Year": src.pages.annual,
    "Basins Total Month": src.pages.accum_mon,
    "Maps Year Mean and STD ": src.pages.map,
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
    st.sidebar.info("The github link can be found "
                    "[here](https://github.com/marcelorodriguesss/analisebacias)")

if __name__ == "__main__":
    main()

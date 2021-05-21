import streamlit as st

import src.pages.accum_mon
import src.pages.annual
import src.pages.map
import src.pages.taylor
import src.pages.correl

PAGES = {
    # "Home": src.pages.home,
    "Correlation": src.pages.correl,
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
    st.sidebar.markdown("""- - - - - - - - - - """)
    st.sidebar.markdown(
        """\#|Name|Spacial Resolution|
        :---:|:---:|:---:|
        1 | Prec | 2.5° x 2.5° |
        2 | PrecL | 2.5° x 2.5° |
        3 | CMAP | 2.5° x 2.5° |
        4 | GPCP | 2.5° x 2.5° |
        5 | GPCC | 0.5° x 0.5° |
        6 | DELAWARE | 0.5° x  0.5° |
        7 | CPC | 0.5° x 0.5° |
        8 | CRU | 0.5° x 0.5° |
        9 | XAVIER | 0.5° x 0.5° |
        10 | REFERENCE | 0.25° x 0.25° |
        11 | CHIRPS | 0.05° x 0.05° |
        """
    )
    st.sidebar.markdown("""- - - - - - - - - - """)
    st.sidebar.info("The github link can be found "
                    "[here](https://github.com/marcelorodriguesss/analisebacias)")

if __name__ == "__main__":
    main()

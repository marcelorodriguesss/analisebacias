import streamlit as st

import src.pages.accum_mon
import src.pages.annual
import src.pages.map
import src.pages.taylor
import src.pages.correl
import src.pages.nash
import src.pages.map_nash_mon
import src.pages.map_nash_yr
import src.pages.map_pearson_mon
import src.pages.map_pearson_yr
import src.pages.cli_mensal
import src.pages.map_thiessen
import src.pages.wavelets


PAGES = {
    "Coef. Correlação Pearson": src.pages.correl,
    "Mapas Correlação Pearson Mensal": src.pages.map_pearson_mon,
    "Mapas Correlação Pearson Anual": src.pages.map_pearson_yr,
    "Coef. Nash Sutcliffe": src.pages.nash,
    "Mapas Nash Sutcliffe Mensal": src.pages.map_nash_mon,
    "Mapas Nash Sutcliffe Anual": src.pages.map_nash_yr,
    "Diagrama de Taylor": src.pages.taylor,
    "Acumulado Anual": src.pages.annual,
    "Acumulado Mensal": src.pages.accum_mon,
    "Climatologia Mensal": src.pages.cli_mensal,
    "Wavelets": src.pages.wavelets,
    "Mapas Thiessen": src.pages.map_thiessen,
    "Mapas Méd. e Desv. Padrão Anual": src.pages.map
}

def main():

    st.sidebar.title("Menu")

    choice = st.sidebar.radio("", list(PAGES.keys()))

    PAGES[choice].main()

    st.sidebar.markdown(
        """\#|Nome|Resolução Espacial|
        :---:|:---:|:---:|
        1 | PRECL | 2.5° x 2.5° |
        2 | CMAP | 2.5° x 2.5° |
        3 | GPCP | 2.5° x 2.5° |
        4 | GPCC | 0.5° x 0.5° |
        5 | DELAWARE | 0.5° x  0.5° |
        6 | CPC | 0.5° x 0.5° |
        7 | CRU | 0.5° x 0.5° |
        8 | CHIRPS | 0.05° x 0.05° |
        9 | REFERENCE | 0.25° x 0.25° |
        """
    )

    # 1 | PREC | 2.5° x 2.5° |
    # 9 | XAVIER | 0.5° x 0.5° |

    st.sidebar.markdown("")
    st.sidebar.info("O código fonte no "
                    "[Github](https://github.com/marcelorodriguesss/analisebacias)")

if __name__ == "__main__":
    main()

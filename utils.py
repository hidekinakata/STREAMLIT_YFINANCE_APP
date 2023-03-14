import base64

import streamlit as st


@st.cache_data()
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
        png_file,
        size=200,
        size_rule='h',
        padding_top=20
):
    binary_string = get_base64_of_bin_file(png_file)

    bg_size = f'{size}px' if size_rule == 'w' else f'auto {size}px'
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64, %s");
                    background-repeat: no-repeat;
                    background-size: %s;
                    padding-top: %spx;
                    background-position-y: %spx;
                    background-position-x: center;
                }
            </style>
            """ % (
        binary_string,
        bg_size,
        size,
        padding_top
    )


def add_logo(png_file, size=100, size_rule='h', padding_top=30):
    logo_markup = build_markup_for_logo(png_file, size, size_rule, padding_top)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

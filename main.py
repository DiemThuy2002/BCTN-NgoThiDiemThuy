import streamlit as st
from streamlit_option_menu import option_menu

import predict
import visualize_h

def main():
    st.markdown("""
        <style>
        .menu-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #FFFFFF;  # White color for menu background
            padding: 5px;
            border-radius: 5px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);  # Adding shadow for depth
            color: #333333;  # Dark grey text color for better contrast on white
        }
        .menu-container .menu-title {
            font-size: 20px;
            font-weight: bold;
        }
        .menu-container .additional-info {
            font-size: 18px;
            color: #3498db;  # Blue for additional info to make it stand out
            font-style: italic;
        }
        </style>
        <div class="menu-container">
            <span class="menu-title">Main Menu</span>
            <span class="additional-info">Edited by: Ngô Thị Diễm Thúy</span>
        </div>
    """, unsafe_allow_html=True)

    app = option_menu(
        menu_title="MAIN MENU",
        options=["Dashboard", "Predict"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "5!important", "background-color": '#FFFFFF', "color": "#333333"},
            "icon": {"color": "grey", "font-size": "23px"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#EEEEEE"},
            "nav-link-selected": {"background-color": "#CCCCCC"},
        }
    )

    if app == "Predict":
        predict.app()
    elif app == "Dashboard":
        visualize_h.main()

if __name__ == "__main__":
    main()

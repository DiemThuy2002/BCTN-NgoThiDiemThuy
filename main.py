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
            background-color: #2c3e50;  # Dark slate color for menu background
            padding: 5px;
            border-radius: 5px;
            color: #ecf0f1;  # Soft white text color
        }
        .menu-container .menu-title {
            font-size: 20px;
            font-weight: bold;
        }
        .menu-container .additional-info {
            font-size: 18px;
            color: #f39c12;  # Bright orange for visibility
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
            "container": {"padding": "5!important", "background-color": '#333333', "color": "#FFFFFF"},
            "icon": {"color": "white", "font-size": "23px"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#444444"},
            "nav-link-selected": {"background-color": "#555555"},
        }
    )

    if app == "Predict":
        predict.app()
    elif app == "Dashboard":
        visualize_h.main()

if __name__ == "__main__":
    main()
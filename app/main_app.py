import streamlit as st
from optimisation.data.loader import charger_villes

def init_app():
    """Configuration initiale"""
    st.set_page_config(
        page_title="Optimisation  de Tournées de Villes",
        page_icon="🗺️",
        layout="wide"
    )
    
    # Charger les données une seule fois
    if 'villes' not in st.session_state:
        st.session_state.villes = charger_villes("villes_france.csv")
    
    # CSS personnalisé
    with open("app/assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if __name__ == "__main__":
    init_app()
    st.success("Application chargée avec succès!")

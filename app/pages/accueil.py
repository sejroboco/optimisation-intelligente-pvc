import streamlit as st

st.set_page_config(
    page_title="Accueil",  # Titre dans l'onglet navigateur
    page_icon="🏠",                  # Icône dans l'onglet
    layout="wide"                   # Optionnel
)

def show():
    st.title("Optimisation de Tournée 🚗💨")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ## Bienvenue dans l'optimisateur de tournées
            
        Cet outil utilise des algorithmes génétiques pour trouver 
        le chemin optimal pour parcourir des villes sélectionnées.
        """)
        
        st.image("app/assets/images/carte_france.jpg", use_container_width=True)
    
    with col2:
        st.info("""
        **Comment utiliser :**
        1. Allez à la page ⚙ Optimisation
        2. Sélectionnez vos villes
        3. Lancez le calcul
        4. Visualisez les résultats 📊
        """)
        
        if st.button("Commencer →"):
            st.switch_page("pages/optim.py")

if __name__ == "__main__":
    show()
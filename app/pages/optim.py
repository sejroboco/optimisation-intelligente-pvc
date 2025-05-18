import streamlit as st
from optimisation.core.algorithme_genetique import AlgorithmeGenetique

st.set_page_config(
    page_title="Optimisation",  # Titre dans l'onglet navigateur
    page_icon="⚙",                  # Icône dans l'onglet
    layout="wide"                   # Optionnel
)

def show():
    st.title("⚙ Paramétrage de l'optimisation")
    
    # Sélection des villes
    noms_villes = [v.nom for v in st.session_state.villes]
    villes_selectionnees = st.multiselect(
        "Sélectionnez les villes à inclure",
        options=noms_villes,
        default=["Paris", "Lyon", "Rennes"]
    )
    
    # Paramètres algorithmiques
    with st.expander("Paramètres avancés"):
        col1, col2 = st.columns(2)
        with col1:
            taille_pop = st.slider("Taille population", 50, 300, 100)
            taux_mut = st.slider("Taux de mutation", 0.01, 0.2, 0.05)
        with col2:
            nb_gen = st.slider("Nombre de générations", 100, 2000, 500)
            taux_elite = st.slider("Élitisme (%)", 5, 30, 10)
    
    # Bouton de lancement
    if st.button("Lancer l'optimisation", type="primary"):
        if len(villes_selectionnees) < 2:
            st.error("Sélectionnez au moins 2 villes")
        else:
            with st.spinner("Optimisation en cours..."):
                villes = [v for v in st.session_state.villes if v.nom in villes_selectionnees]
                
                algo = AlgorithmeGenetique(
                    villes=villes,
                    taille_population=taille_pop,
                    taux_mutation=taux_mut,
                    nb_generations=nb_gen,
                    taux_elitisme=taux_elite/100
                )
                
                st.session_state.meilleur, st.session_state.historique = algo.executer()
                st.switch_page("pages/resultats.py")

if __name__ == "__main__":
    show()
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Résultats",  # Titre dans l'onglet navigateur
    page_icon="📊",                  # Icône dans l'onglet
    layout="wide"                   # Optionnel
)

def show():
    st.title("📊 Résultats de l'optimisation")
    
    if 'meilleur' not in st.session_state:
        st.warning("Aucun résultat disponible. Lancez d'abord une optimisation.")
        st.page_link("pages/optim.py", label="← Retour à l'optimisation")
        return
    
    # Métriques principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Distance totale", f"{st.session_state.meilleur.distance_totale():.2f} km")
    with col2:
        st.metric("Villes visitées", len(st.session_state.meilleur.ordre))
    with col3:
        st.metric("Générations calculées", len(st.session_state.historique))
    
    # Cartographie
    st.subheader("Itinéraire optimal")
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    
    # Ajout des marqueurs
    for i, ville in enumerate(st.session_state.meilleur.ordre):
        folium.Marker(
            location=[ville.latitude, ville.longitude],
            popup=f"{i+1}. {ville.nom}",
            icon=folium.Icon(color="red" if i==0 else "blue")
        ).add_to(m)
    
    # Tracé de l'itinéraire
    coords = [[v.latitude, v.longitude] for v in st.session_state.meilleur.ordre]
    coords.append(coords[0])  # Bouclage
    folium.PolyLine(coords, color="green", weight=2.5, opacity=1).add_to(m)
    
    st_folium(m, width=1000, height=400)
    
    # Détails textuels
    with st.expander("Voir l'itinéraire détaillé"):
        for i, ville in enumerate(st.session_state.meilleur.ordre, 1):
            st.write(f"{i}. {ville.nom} ({ville.latitude:.4f}, {ville.longitude:.4f})")
    
    # Graphique d'évolution
    st.subheader("Progression de l'algorithme")
    st.line_chart(pd.DataFrame(st.session_state.historique, columns=["Distance"]))

if __name__ == "__main__":
    show()
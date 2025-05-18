#!/usr/bin/env python3
"""
Script principal pour résoudre le problème du voyageur de commerce
avec un algorithme génétique.
"""

from optimisation.core.ville import Ville
from optimisation.core.itineraire import Itineraire
from algorithme_genetique import AlgorithmeGenetique
from optimisation.data.loader import charger_villes
import matplotlib.pyplot as plt
import pandas as pd
import time
import argparse
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../utilis/loggerlogs/execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def configurer_arguments():
    """Configure les arguments en ligne de commande"""
    parser = argparse.ArgumentParser(description="Résolution TSP avec algorithme génétique")
    parser.add_argument('--fichier', type=str, default='data/villes_france.csv',
                      help='Chemin vers le fichier CSV des villes')
    parser.add_argument('--max_villes', type=int, default=None,
                      help='Nombre maximum de villes à considérer')
    parser.add_argument('--population', type=int, default=1000,
                      help='Taille de la population')
    parser.add_argument('--generations', type=int, default=500,
                      help='Nombre de générations')
    parser.add_argument('--mutation', type=float, default=0.05,
                      help='Taux de mutation')
    parser.add_argument('--elitisme', type=float, default=0.1,
                      help='Taux d\'élitisme')
    parser.add_argument('--visualiser', action='store_true',
                      help='Afficher les visualisations')
    return parser.parse_args()

def visualiser_resultats(meilleur_itineraire, historique):
    """Génère les visualisations des résultats"""
    plt.figure(figsize=(12, 6))
    
    # Graphique d'évolution
    plt.subplot(1, 2, 1)
    plt.plot(historique, 'b-', linewidth=1)
    plt.title('Évolution de la distance')
    plt.xlabel('Génération')
    plt.ylabel('Distance (km)')
    plt.grid(True)
    
    # Carte des villes
    plt.subplot(1, 2, 2)
    x = [ville.longitude for ville in meilleur_itineraire.ordre]
    y = [ville.latitude for ville in meilleur_itineraire.ordre]
    x.append(x[0])  # Retour à la première ville
    y.append(y[0])
    
    plt.plot(x, y, 'ro-')
    plt.title('Itinéraire optimal')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('results/itineraire_optimal.png')
    plt.show()

def sauvegarder_resultats(meilleur_itineraire, historique, temps_execution):
    """Sauvegarde les résultats dans des fichiers"""
    Path('results').mkdir(exist_ok=True)
    
    # Sauvegarde texte
    with open('results/meilleur_itineraire.txt', 'w') as f:
        f.write(f"Distance optimale: {meilleur_itineraire.distance_totale():.2f} km\n")
        f.write(f"Temps d'exécution: {temps_execution:.2f} secondes\n\n")
        f.write("Itinéraire:\n")
        for i, ville in enumerate(meilleur_itineraire.ordre, 1):
            f.write(f"{i}. {ville.nom}\n")
    
    # Sauvegarde des données
    pd.DataFrame({
        'generation': range(len(historique)),
        'distance': historique
    }).to_csv('results/historique_evolution.csv', index=False)

def main():
    args = configurer_arguments()
    
    try:
        logger.info("========== Début du programme ==========")
        
        # 1. Chargement des données
        logger.info(f"Chargement des villes depuis {args.fichier}")
        villes = charger_villes(
            path=args.fichier,
            max_villes=args.max_villes,
            sample=False
        )
        
        if not villes:
            logger.error("Aucune ville chargée - vérifiez votre fichier d'entrée")
            return
        
        # 2. Configuration de l'algorithme
        logger.info("Initialisation de l'algorithme génétique")
        config = {
            'taille_population': args.population,
            'taux_mutation': args.mutation,
            'nb_generations': args.generations,
            'taux_elitisme': args.elitisme
        }
        
        # 3. Exécution
        logger.info("Démarrage de l'optimisation")
        debut = time.time()
        
        ag = AlgorithmeGenetique(villes, **config)
        meilleur, historique = ag.executer()
        
        temps_execution = time.time() - debut
        
        # 4. Résultats
        logger.info(f"Optimisation terminée en {temps_execution:.2f} secondes")
        logger.info(f"Distance optimale: {meilleur.distance_totale():.2f} km")
        
        # 5. Sauvegarde et visualisation
        sauvegarder_resultats(meilleur, historique, temps_execution)
        
        if args.visualiser:
            visualiser_resultats(meilleur, historique)
            
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {str(e)}", exc_info=True)
    finally:
        logger.info("========== Programme terminé ==========")

if __name__ == "__main__":
    main()
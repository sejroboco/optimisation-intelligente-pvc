from optimisation.core.ville import Ville
from optimisation.core.itineraire import Itineraire
import random
from typing import List, Tuple
import copy

class AlgorithmeGenetique:
    def __init__(self, villes: List['Ville'],
                 taille_population: int = 100, 
                 taux_mutation: float = 0.01,
                 nb_generations: int = 500,
                 taux_elitisme: float = 0.1):
        """
        Args:
            villes: Liste des villes à visiter
            taille_population: Nombre d'individus dans la population
            taux_mutation: Probabilité de mutation pour chaque ville
            nb_generations: Nombre maximum de générations
            taux_elitisme: Pourcentage des meilleurs à conserver directement
        """
        self.villes = villes
        self.taille_population = taille_population
        self.taux_mutation = taux_mutation
        self.nb_generations = nb_generations
        self.taux_elitisme = taux_elitisme
        self.population = self._initialiser_population()
        
    def _initialiser_population(self) -> List[Itineraire]:
        """Crée la population initiale aléatoire"""
        return [Itineraire(self.villes) for _ in range(self.taille_population)]
    
    def selection_par_tournoi(self, k: int = 3) -> Itineraire:
        """Sélection par tournoi de k individus"""
        participants = random.sample(self.population, k)
        return min(participants, key=lambda x: x.distance_totale())
    
    def croisement_OX(self, parent1: Itineraire, parent2: Itineraire) -> Itineraire:
        """Ordered Crossover (OX) pour le TSP"""
        taille = len(parent1.ordre)
        a, b = sorted(random.sample(range(taille), 2))
        
        # Créer le génome de l'enfant
        enfant_ordre = [None] * taille
        
        # Copier le segment entre a et b du parent1
        enfant_ordre[a:b] = parent1.ordre[a:b]
        
        # Remplir le reste avec les villes du parent2 dans l'ordre
        current_pos = b % taille
        for ville in parent2.ordre[b:] + parent2.ordre[:b]:
            if ville not in enfant_ordre:
                while enfant_ordre[current_pos % taille] is not None:
                    current_pos += 1
                enfant_ordre[current_pos % taille] = ville
                current_pos += 1
        
        # Créer le nouvel itinéraire
        nouvel_itineraire = Itineraire(self.villes)
        nouvel_itineraire.ordre = enfant_ordre
        nouvel_itineraire._distance = None  # Réinitialiser le cache
        return nouvel_itineraire
    
    def mutation_echange(self, itineraire: Itineraire):
        """Mutation par échange de deux villes"""
        if random.random() < self.taux_mutation:
            i, j = random.sample(range(len(itineraire.ordre)), 2)
            itineraire.ordre[i], itineraire.ordre[j] = itineraire.ordre[j], itineraire.ordre[i]
            itineraire._distance = None  # Invalider le cache
    
    def _selection_elites(self) -> List[Itineraire]:
        """Sélectionne les meilleurs individus selon le taux d'élitisme"""
        n_elites = max(1, int(self.taille_population * self.taux_elitisme))
        return sorted(self.population, key=lambda x: x.distance_totale())[:n_elites]
    
    def evoluer(self):
        """Fait évoluer la population sur une génération"""
        elites = self._selection_elites()
        nouvelle_population = elites.copy()
        
        while len(nouvelle_population) < self.taille_population:
            parent1 = self.selection_par_tournoi()
            parent2 = self.selection_par_tournoi()
            enfant = self.croisement_OX(parent1, parent2)
            self.mutation_echange(enfant)
            nouvelle_population.append(enfant)
        
        self.population = nouvelle_population
    
    def executer(self) -> Tuple[Itineraire, List[float]]:
        """
        Exécute l'algorithme génétique
        
        Returns:
            Tuple: (meilleur itinéraire, historique des distances)
        """
        historique_distances = []
        
        for generation in range(self.nb_generations):
            self.evoluer()
            meilleur = min(self.population, key=lambda x: x.distance_totale())
            historique_distances.append(meilleur.distance_totale())
            
            if generation % 50 == 0:
                print(f"Génération {generation}: Distance = {meilleur.distance_totale():.2f}")
        
        return self.meilleur_itineraire(), historique_distances
    
    def meilleur_itineraire(self) -> Itineraire:
        """Retourne le meilleur itinéraire de la population actuelle"""
        return min(self.population, key=lambda x: x.distance_totale())
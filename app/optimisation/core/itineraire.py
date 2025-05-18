import random
from typing import List  # Pour le type hinting
from optimisation.core.ville import Ville

class Itineraire:
    def __init__(self, villes: List['Ville']):
        """
        Args:
            villes: Liste d'objets Ville
        """
        if not villes:
            raise ValueError("La liste de villes ne peut pas être vide")
            
        self.villes = villes.copy()  # Évite les effets de bord
        self.ordre = random.sample(self.villes, len(self.villes))
        self._distance = None  # Cache pour la distance
        
    def distance_totale(self) -> float:
        """Calcule la distance totale de l'itinéraire avec mise en cache."""
        if self._distance is None:
            distance = 0.0
            for i in range(len(self.ordre)):
                ville_actuelle = self.ordre[i]
                ville_suivante = self.ordre[(i + 1) % len(self.ordre)]
                distance += ville_actuelle.distance_vers(ville_suivante)
            self._distance = distance
        return self._distance
    
    def invalidate_cache(self):
        """Réinitialise le cache de distance."""
        self._distance = None
        
    def __str__(self):
        noms_villes = [ville.nom for ville in self.ordre]
        return f"Itinéraire ({len(noms_villes)} villes): " + " -> ".join(noms_villes)
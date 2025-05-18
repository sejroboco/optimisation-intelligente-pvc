from math import radians, sin, cos, sqrt, atan2

class Ville:
    def __init__(self, nom, latitude, longitude):
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude

    def distance_vers(self, autre_ville):
        """
        Calcule la distance en kilomètres entre cette ville et une autre ville
        en utilisant la formule de Haversine.
        
        Args:
            autre_ville (Ville): L'autre ville vers laquelle calculer la distance
            
        Returns:
            float: Distance en kilomètres
        """
        # Rayon de la Terre en kilomètres
        R = 6371.0
        
        # Conversion des degrés en radians
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(autre_ville.latitude)
        lon2 = radians(autre_ville.longitude)
        
        # Différences de coordonnées
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Formule de Haversine
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        
        return distance

    def __repr__(self):
        return f"Ville({self.nom}, lat={self.latitude}, lon={self.longitude})"


# # Exemple d'utilisation
# if __name__ == "__main__":
#     paris = Ville("Paris", 48.8566, 2.3522)
#     lyon = Ville("Lyon", 45.7640, 4.8357)
    
#     distance = paris.distance_vers(lyon)
#     print(f"Distance entre {paris.nom} et {lyon.nom}: {distance:.2f} km")
#     # Devrait afficher environ 392.22 km
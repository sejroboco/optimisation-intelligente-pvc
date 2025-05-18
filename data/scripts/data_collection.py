import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

villes = [
    # France métropolitaine
    'Paris', 'Lyon', 'Marseille', 'Lille', 'Bordeaux', 'Toulouse', 'Nantes',
    'Strasbourg', 'Montpellier', 'Rennes', 'Nice', 'Dijon', 'Le Havre', 'Grenoble', 'Reims',
    'Saint-Étienne', 'Toulon', 'Angers', 'Clermont-Ferrand', 'Brest', 'Le Mans', 'Amiens',
    'Limoges', 'Tours', 'Villeurbanne', 'Metz', 'Besançon', 'Caen', 'Orléans', 'Mulhouse',
    'Rouen', 'Perpignan', 'Nancy', 'Argenteuil', 'Montreuil', 'Saint-Denis', 'Roubaix',
    'Avignon', 'Tourcoing', 'Fort-de-France', 'Poitiers', 'Versailles', 'Créteil', 'Pau',
    'Colombes', 'Aulnay-sous-Bois', 'Rueil-Malmaison', 'La Rochelle', 'Antibes', 'Saint-Maur-des-Fossés',
    'Calais', 'Champigny-sur-Marne', 'Saint-Nazaire', 'Dunkerque', 'Aix-en-Provence', 'Béziers',
    'Bourges', 'Cannes', 'Courbevoie', 'Saint-Quentin', 'Valence', 'Quimper', 'Ajaccio',
    'Levallois-Perret', 'Issy-les-Moulineaux', 'Neuilly-sur-Seine', 'Troyes', 'Antony', 'Villeneuve-d\'Ascq',
    'Sarcelles', 'Pessac', 'Évry', 'Vénissieux', 'Clichy', 'Cergy', 'Saint-André', 'Ivry-sur-Seine',
    'Chambéry', 'Lorient', 'Montauban', 'Sartrouville', 'Niort', 'Villejuif', 'Meaux', 'Bayonne',
    'Hyères', 'Épinay-sur-Seine', 'Pantin', 'Bondy', 'Maisons-Alfort', 'Chelles', 'Fontenay-sous-Bois',
    'Arles', 'Fréjus', 'Sèvres', 'Vannes', 'Évry-Courcouronnes', 'Brive-la-Gaillarde', 'Saint-Ouen',
    
    # Outre-mer
    'Saint-Denis (La Réunion)', 'Saint-Pierre (La Réunion)', 
    'Papeete (Tahiti)', 'Mamoudzou (Mayotte)',
    'Cayenne (Guyane)', 'Basse-Terre (Guadeloupe)', 'Fort-de-France (Martinique)'
]

geolocator = Nominatim(user_agent="tsp_france")

def get_location(ville, retries=3):
    for i in range(retries):
        try:
            return geolocator.geocode(ville + ", France", timeout=10)
        except GeocoderTimedOut:
            print(f"[{ville}] Timeout. Nouvelle tentative ({i+1}/{retries})...")
            time.sleep(2)
    return None  # Si toujours échoué

data = []
for ville in villes:
    location = get_location(ville)
    if location:
        data.append((ville, location.latitude, location.longitude))
        print(f"{ville} -> {location.latitude}, {location.longitude}")
    else:
        print(f"⚠️ Pas trouvé : {ville}")
    time.sleep(1.5)  # Toujours respecter le quota

df = pd.DataFrame(data, columns=["ville", "latitude", "longitude"])
df.to_csv("../villes_france.csv", index=False)

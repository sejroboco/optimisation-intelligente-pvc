import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

# === Chargement des villes ===
df = pd.read_csv("../villes_france.csv")

villes = ['Paris', 'Lyon', 'Marseille', 'Lille', 'Bordeaux', 'Toulouse', 'Nantes',
          'Strasbourg', 'Montpellier', 'Rennes', 'Nice', 'Dijon', 'Le Havre', 'Grenoble', 'Reims']

# === Haversine ===
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Rayon de la Terre en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# === Euclidienne ===
def euclidean(lat1, lon1, lat2, lon2):
    return sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

# === Matrices de distances ===
n = len(df)
dist_haversine = np.zeros((n, n))
dist_euclidean = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        lat1, lon1 = df.iloc[i][["latitude", "longitude"]]
        lat2, lon2 = df.iloc[j][["latitude", "longitude"]]
        dist_haversine[i, j] = haversine(lat1, lon1, lat2, lon2)
        dist_euclidean[i, j] = euclidean(lat1, lon1, lat2, lon2)

# Convertir en DataFrame lisibles
cities = df["ville"].tolist()
df_haversine = pd.DataFrame(dist_haversine, index=cities, columns=cities)
df_euclidean = pd.DataFrame(dist_euclidean, index=cities, columns=cities)

# Enregistrement des DataFrames
df_haversine.to_csv("../distances_euclidiennes.csv", index=villes)
df_euclidean.to_csv("../distances_haversine.csv", index=villes)


# Affichage optionnel
print("Distance Haversine (km):")
print(df_haversine.round(2))

print("\nDistance Euclidienne (approx):")
print(df_euclidean.round(4))

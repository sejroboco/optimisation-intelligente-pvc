from pathlib import Path
import pandas as pd
from typing import List
from optimisation.core.ville import Ville

def charger_villes(path: str, max_villes: int = None, sample: bool = False) -> List[Ville]:
    """Charge les villes depuis un CSV avec gestion robuste des erreurs."""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Le fichier {path} n'existe pas")
            
        df = pd.read_csv(path_obj)
        
        # Validation des colonnes
        required_cols = {'ville', 'latitude', 'longitude'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            raise ValueError(f"Colonnes manquantes: {missing}")
        
        # Nettoyage des données
        df = df.dropna(subset=['latitude', 'longitude'])
        
        # Sélection des villes
        if max_villes is not None:
            df = df.sample(max_villes) if sample else df.head(max_villes)
            
        return [
            Ville(nom=row['ville'], 
                 latitude=float(row['latitude']), 
                 longitude=float(row['longitude']))
            for _, row in df.iterrows()
        ]
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {str(e)}")
        raise
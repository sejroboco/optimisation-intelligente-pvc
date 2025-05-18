import unittest
from optimisation.core.ville import Ville
from optimisation.data.loader import charger_villes
import os

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Crée un petit CSV temporaire pour les tests
        self.test_csv = "test_villes.csv"
        with open(self.test_csv, "w") as f:
            f.write("nom,latitude,longitude\n")
            f.write("Paris,48.8566,2.3522\n")
            f.write("Lyon,45.7640,4.8357\n")

    def tearDown(self):
        # Supprime le fichier temporaire après test
        os.remove(self.test_csv)

    def test_charger_villes(self):
        villes = charger_villes(self.test_csv)
        self.assertEqual(len(villes), 2)
        self.assertIsInstance(villes[0], Ville)
        self.assertEqual(villes[0].nom, "Paris")
        self.assertAlmostEqual(villes[0].latitude, 48.8566)
        self.assertAlmostEqual(villes[0].longitude, 2.3522)

if __name__ == "__main__":
    unittest.main()

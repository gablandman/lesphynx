import requests
import time

API_URL = "http://localhost:8001"

def test_game():
    print("1. Réinitialisation du jeu...")
    requests.post(f"{API_URL}/reset")
    time.sleep(0.5)
    
    print("2. Placement du cochonnet...")
    requests.post(f"{API_URL}/cochonnet/place", params={"x": 0, "z": 8})
    time.sleep(1)
    
    print("3. Lancer de la première boule (joueur 1)...")
    requests.post(f"{API_URL}/ball/throw", json={
        "player": "Joueur1",
        "force": 0.7,
        "angle_horizontal": 5,
        "angle_vertical": 15,
        "effect": 0.1
    })
    time.sleep(3)
    
    print("4. Lancer de la deuxième boule (joueur 2)...")
    requests.post(f"{API_URL}/ball/throw", json={
        "player": "Joueur2",
        "force": 0.8,
        "angle_horizontal": -3,
        "angle_vertical": 12,
        "effect": -0.2
    })
    time.sleep(3)
    
    print("5. Récupération des distances...")
    response = requests.get(f"{API_URL}/distances")
    distances = response.json()
    print("Distances:", distances)
    
    print("\nTest terminé! Ouvrez visualizer.html dans votre navigateur pour voir le résultat.")

if __name__ == "__main__":
    test_game()
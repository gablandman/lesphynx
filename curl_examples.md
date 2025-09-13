# Exemples de commandes CURL pour le simulateur de pétanque

## 1. Réinitialiser la partie
```bash
curl -X POST http://localhost:8001/reset
```

## 2. Placer le cochonnet
```bash
# Au centre à 8m
curl -X POST "http://localhost:8001/cochonnet/place?x=0&z=8"

# Décalé à droite à 10m
curl -X POST "http://localhost:8001/cochonnet/place?x=1.5&z=10"

# À gauche à 6m
curl -X POST "http://localhost:8001/cochonnet/place?x=-1&z=6"
```

## 3. Lancer une boule
```bash
# Tir simple
curl -X POST http://localhost:8001/ball/throw \
  -H "Content-Type: application/json" \
  -d '{
    "player": "Joueur1",
    "force": 0.7,
    "angle_horizontal": 0,
    "angle_vertical": 15,
    "effect": 0
  }'

# Tir avec effet à droite
curl -X POST http://localhost:8001/ball/throw \
  -H "Content-Type: application/json" \
  -d '{
    "player": "Joueur2",
    "force": 0.6,
    "angle_horizontal": 10,
    "angle_vertical": 20,
    "effect": 0.5
  }'

# Tir puissant (pour dégager)
curl -X POST http://localhost:8001/ball/throw \
  -H "Content-Type: application/json" \
  -d '{
    "player": "Joueur1",
    "force": 1.0,
    "angle_horizontal": 0,
    "angle_vertical": 8,
    "effect": 0
  }'

# Tir en cloche
curl -X POST http://localhost:8001/ball/throw \
  -H "Content-Type: application/json" \
  -d '{
    "player": "Joueur2",
    "force": 0.5,
    "angle_horizontal": -3,
    "angle_vertical": 45,
    "effect": -0.2
  }'
```

## 4. Obtenir l'état du jeu
```bash
curl -X GET http://localhost:8001/state
```

## 5. Obtenir les distances
```bash
curl -X GET http://localhost:8001/distances
```

## 6. Vérifier la santé du serveur
```bash
curl -X GET http://localhost:8001/health
```

## Paramètres des lancers

- **player**: Nom du joueur (string)
- **force**: Force du lancer (0.0 à 1.0)
  - 0.3-0.5 : Lancer doux
  - 0.6-0.8 : Lancer normal
  - 0.9-1.0 : Lancer fort
- **angle_horizontal**: Angle horizontal en degrés (-30 à 30)
  - Négatif : vers la gauche
  - Positif : vers la droite
- **angle_vertical**: Angle vertical en degrés (0 à 90)
  - 5-15 : Tir tendu
  - 20-35 : Tir normal
  - 40-90 : Tir en cloche
- **effect**: Effet latéral (-1.0 à 1.0)
  - Négatif : courbe vers la gauche
  - Positif : courbe vers la droite
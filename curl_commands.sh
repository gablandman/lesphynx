#!/bin/bash

# Réinitialiser la partie
echo "=== Réinitialisation de la partie ==="
curl -X POST http://localhost:8001/reset
echo -e "\n"
sleep 2

# Placer le cochonnet au centre à 8m
echo "=== Placement du cochonnet ==="
curl -X POST "http://localhost:8001/cochonnet/place?x=0&z=8"
echo -e "\n"
sleep 10

# Lancer une boule (Joueur 1) - tir droit
echo "=== Lancer Joueur 1 - Tir droit ==="
curl -X POST http://localhost:8001/ball/throw \
  -H "Content-Type: application/json" \
  -d '{
    "player": "Joueur1",
    "force": 0.85,
    "angle_horizontal": 0,
    "angle_vertical": 30,
    "effect": 0
  }'
echo -e "\n"
sleep 10

# Lancer une boule (Joueur 2) - avec effet à gauche
echo "=== Lancer Joueur 2 - Effet gauche ==="
curl -X POST http://localhost:8001/ball/throw \
  -H "Content-Type: application/json" \
  -d '{
    "player": "Joueur2",
    "force": 0.9,
    "angle_horizontal": -5,
    "angle_vertical": 28,
    "effect": -0.2
  }'
echo -e "\n"
sleep 10

# Lancer une boule (Joueur 1) - tir moyen
echo "=== Lancer Joueur 1 - Tir moyen ==="
curl -X POST http://localhost:8001/ball/throw \
  -H "Content-Type: application/json" \
  -d '{
    "player": "Joueur1",
    "force": 0.95,
    "angle_horizontal": 2,
    "angle_vertical": 25,
    "effect": 0.1
  }'
echo -e "\n"
sleep 10

# Obtenir l'état du jeu
echo "=== État actuel du jeu ==="
curl -X GET http://localhost:8001/state | python3 -m json.tool
echo -e "\n"
sleep 2

# Obtenir les distances
echo "=== Distances au cochonnet ==="
curl -X GET http://localhost:8001/distances | python3 -m json.tool
echo -e "\n"
sleep 2

# Vérifier la santé du serveur
echo "=== Santé du serveur ==="
curl -X GET http://localhost:8001/health | python3 -m json.tool
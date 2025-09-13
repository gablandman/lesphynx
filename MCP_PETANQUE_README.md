# Serveur MCP pour Simulateur de Pétanque 3D

## Vue d'ensemble

Ce serveur MCP permet de contrôler le simulateur de pétanque 3D via des commandes naturelles depuis Claude ou tout autre client MCP.

## Installation et lancement

1. **Installer les dépendances** :
```bash
uv lock
uv sync
```

2. **Lancer le simulateur de pétanque** (port 8001) :
```bash
uv run petanque_server.py
```

3. **Ouvrir le visualisateur** :
Ouvrir `visualizer.html` dans un navigateur web

4. **Lancer le serveur MCP** (port 3000) :
```bash
uv run mcp_petanque_server.py
```

## Tools disponibles

### 1. **reset_game**
Réinitialise complètement la partie.
```
Exemple: "Réinitialise la partie de pétanque"
```

### 2. **place_cochonnet**
Place le cochonnet sur le terrain.
- `x` : Position horizontale (-2 à 2)
- `z` : Distance (6 à 12 mètres)
```
Exemple: "Place le cochonnet au centre à 8 mètres"
```

### 3. **throw_ball**
Lance une boule avec des paramètres précis.
- `player` : Nom du joueur
- `force` : Force du lancer (0.1 à 1.0)
- `angle_horizontal` : Angle gauche/droite (-30 à 30)
- `angle_vertical` : Angle de tir (5 à 80)
- `effect` : Effet latéral (-1 à 1)
```
Exemple: "Lance une boule pour Alice avec une force moyenne"
```

### 4. **get_game_state**
Récupère l'état complet du jeu.
```
Exemple: "Montre-moi l'état actuel du jeu"
```

### 5. **get_distances**
Obtient les distances de toutes les boules au cochonnet.
```
Exemple: "Quelles sont les distances au cochonnet ?"
```

## Resources MCP

- `petanque://state` : État complet du jeu en JSON
- `petanque://distances` : Distances au cochonnet en JSON

## Prompts MCP

- `strategy` : Suggère une stratégie basée sur la situation
- `beginner` : Conseils pour débutants

## Exemples d'utilisation avec Claude

```
"Commence une nouvelle partie de pétanque"
"Place le cochonnet à droite à 9 mètres"
"Lance une boule douce pour Marie"
"Montre-moi qui est le plus proche"
"Lance un tir fort pour dégager la boule adverse"
"Quelle stratégie me conseilles-tu ?"
```

## Configuration dans Claude Desktop

Ajouter dans `claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "petanque": {
      "command": "uv",
      "args": ["run", "mcp_petanque_server.py"],
      "transport": "streamable-http",
      "httpUrl": "http://localhost:3000/mcp"
    }
  }
}
```

## Paramètres de lancer

### Force
- 0.1-0.3 : Très doux (pointer précis)
- 0.4-0.6 : Moyen (approche normale)
- 0.7-0.9 : Fort (dégager/tirer)
- 1.0 : Maximum (tir puissant)

### Angle vertical
- 5-15° : Tir tendu/rasant
- 20-35° : Tir normal
- 40-60° : Tir en cloche
- 60-80° : Tir très haut

### Angle horizontal
- -30 à -10 : Fort vers la gauche
- -10 à -5 : Légèrement à gauche
- -5 à 5 : Droit devant
- 5 à 10 : Légèrement à droite
- 10 à 30 : Fort vers la droite

### Effet
- -1.0 : Courbe maximale vers la gauche
- -0.5 : Effet gauche modéré
- 0 : Aucun effet
- 0.5 : Effet droite modéré
- 1.0 : Courbe maximale vers la droite
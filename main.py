"""
MCP Server pour le simulateur de Pétanque 3D
"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field
import mcp.types as types
import requests
import json
from typing import Dict, List, Optional
import time

mcp = FastMCP("Pétanque Simulator MCP", port=3000, stateless_http=True, debug=True)

API_URL = "http://localhost:8001"

@mcp.tool(
    title="Réinitialiser la partie",
    description="Réinitialise complètement la partie de pétanque en effaçant toutes les boules et le cochonnet",
)
async def reset_game() -> str:
    """Réinitialise la partie de pétanque"""
    try:
        response = requests.post(f"{API_URL}/reset")
        response.raise_for_status()
        return "Partie réinitialisée avec succès. Le terrain est maintenant vide."
    except Exception as e:
        return f"Erreur lors de la réinitialisation: {str(e)}"

@mcp.tool(
    title="Placer le cochonnet",
    description="Place le cochonnet sur le terrain à une position spécifique",
)
async def place_cochonnet(
    x: float = Field(description="Position horizontale (gauche/droite) entre -2 et 2", ge=-2, le=2),
    z: float = Field(description="Distance depuis la ligne de lancer entre 6 et 12 mètres", ge=6, le=12)
) -> str:
    """Place le cochonnet sur le terrain"""
    try:
        response = requests.post(f"{API_URL}/cochonnet/place", params={"x": x, "z": z})
        response.raise_for_status()
        return f"Cochonnet placé avec succès à la position x={x}, z={z}"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            return "Position invalide pour le cochonnet. Assurez-vous que x est entre -2 et 2, et z entre 6 et 12."
        return f"Erreur HTTP: {str(e)}"
    except Exception as e:
        return f"Erreur lors du placement du cochonnet: {str(e)}"

@mcp.tool(
    title="Lancer une boule",
    description="Lance une boule de pétanque avec des paramètres spécifiques",
)
async def throw_ball(
    player: str = Field(description="Nom du joueur qui lance"),
    force: float = Field(description="Force du lancer (0.1=très doux, 0.5=moyen, 1.0=très fort)", ge=0.1, le=1.0, default=0.5),
    angle_horizontal: float = Field(description="Angle horizontal en degrés (-30=gauche, 0=droit, 30=droite)", ge=-30, le=30, default=0),
    angle_vertical: float = Field(description="Angle vertical en degrés (10=tendu, 30=normal, 60=cloche)", ge=5, le=80, default=25),
    effect: float = Field(description="Effet latéral (-1=courbe gauche, 0=droit, 1=courbe droite)", ge=-1, le=1, default=0)
) -> str:
    """Lance une boule avec les paramètres spécifiés"""
    try:
        data = {
            "player": player,
            "force": force,
            "angle_horizontal": angle_horizontal,
            "angle_vertical": angle_vertical,
            "effect": effect
        }
        response = requests.post(f"{API_URL}/ball/throw", json=data)
        response.raise_for_status()
        
        # Attendre que la boule s'arrête
        time.sleep(5)
        
        # Obtenir les distances après le lancer
        distances_response = requests.get(f"{API_URL}/distances")
        if distances_response.ok:
            distances = distances_response.json().get("distances", [])
            if distances:
                last_ball = distances[-1]
                return f"Boule lancée par {player}. Distance au cochonnet: {last_ball['distance']:.2f}m"
        
        return f"Boule lancée avec succès par {player}"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            return "Erreur: Le cochonnet doit être placé avant de lancer une boule."
        return f"Erreur HTTP: {str(e)}"
    except Exception as e:
        return f"Erreur lors du lancer: {str(e)}"

@mcp.tool(
    title="Obtenir l'état du jeu",
    description="Récupère l'état complet du jeu incluant les positions de toutes les boules et du cochonnet",
)
async def get_game_state() -> str:
    """Obtient l'état actuel du jeu"""
    try:
        response = requests.get(f"{API_URL}/state")
        response.raise_for_status()
        state = response.json()
        
        result = []
        result.append(f"Phase de jeu: {state['game_phase']}")
        
        if state['cochonnet']:
            pos = state['cochonnet']['position']
            result.append(f"Cochonnet: x={pos[0]:.2f}, z={pos[2]:.2f}")
        
        if state['balls']:
            result.append(f"\nNombre de boules: {len(state['balls'])}")
            for ball in state['balls']:
                pos = ball['position']
                result.append(f"- {ball['player']}: x={pos[0]:.2f}, z={pos[2]:.2f}")
        
        return "\n".join(result)
    except Exception as e:
        return f"Erreur lors de la récupération de l'état: {str(e)}"

@mcp.tool(
    title="Obtenir les distances",
    description="Récupère les distances de toutes les boules au cochonnet, triées de la plus proche à la plus éloignée",
)
async def get_distances() -> str:
    """Obtient les distances au cochonnet"""
    try:
        response = requests.get(f"{API_URL}/distances")
        response.raise_for_status()
        data = response.json()
        distances = data.get("distances", [])
        
        if not distances:
            return "Aucune boule n'a été lancée."
        
        result = ["Distances au cochonnet (du plus proche au plus éloigné):"]
        for i, item in enumerate(distances, 1):
            result.append(f"{i}. {item['player']}: {item['distance']:.3f}m")
        
        return "\n".join(result)
    except Exception as e:
        return f"Erreur lors de la récupération des distances: {str(e)}"

@mcp.resource(
    uri="petanque://state",
    description="État actuel complet du jeu de pétanque",
    name="État du jeu",
)
async def get_state_resource() -> str:
    """Fournit l'état actuel du jeu sous forme de ressource"""
    try:
        response = requests.get(f"{API_URL}/state")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.resource(
    uri="petanque://distances",
    description="Distances de toutes les boules au cochonnet",
    name="Distances au cochonnet",
)
async def get_distances_resource() -> str:
    """Fournit les distances sous forme de ressource"""
    try:
        response = requests.get(f"{API_URL}/distances")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.prompt("strategy")
async def suggest_strategy(
    situation: str = Field(description="Description de la situation actuelle (ex: 'adversaire a 2 boules proches')")
) -> str:
    """Suggère une stratégie de jeu basée sur la situation"""
    
    # Obtenir l'état actuel
    try:
        state_response = requests.get(f"{API_URL}/state")
        distances_response = requests.get(f"{API_URL}/distances")
        
        if state_response.ok and distances_response.ok:
            state = state_response.json()
            distances = distances_response.json().get("distances", [])
            
            context = f"""Tu es un expert en pétanque. Voici la situation actuelle:
            
Cochonnet: {state.get('cochonnet', {}).get('position', 'non placé')}
Nombre de boules jouées: {len(state.get('balls', []))}
Distances au cochonnet: {distances}

Situation décrite: {situation}

Suggère une stratégie de jeu détaillée incluant:
1. Le type de tir recommandé (pointer, tirer, etc.)
2. Les paramètres suggérés (force, angles, effet)
3. La justification tactique
"""
            return context
        else:
            return f"Analyse la situation de pétanque suivante et suggère une stratégie: {situation}"
    except:
        return f"Analyse la situation de pétanque suivante et suggère une stratégie: {situation}"

@mcp.prompt("beginner")
async def beginner_tips() -> str:
    """Fournit des conseils pour les débutants"""
    return """Tu es un coach de pétanque bienveillant. Donne des conseils pour bien débuter:

1. Comment tenir et lancer une boule
2. Les différents types de lancers (pointer vs tirer)
3. Les règles de base
4. Les erreurs courantes à éviter
5. Comment choisir sa force et ses angles

Sois encourageant et pédagogue."""

if __name__ == "__main__":
    print("Démarrage du serveur MCP Pétanque sur le port 3000...")
    print("Assurez-vous que le serveur de pétanque est lancé sur le port 8001")
    mcp.run(transport="streamable-http")
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Tuple
import numpy as np
from enum import Enum
import asyncio
from datetime import datetime

app = FastAPI(title="Pétanque 3D Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BallType(str, Enum):
    BOULE = "boule"
    COCHONNET = "cochonnet"

class Ball(BaseModel):
    id: str
    type: BallType
    position: Tuple[float, float, float]
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    player: Optional[str] = None
    color: Optional[str] = None

class ThrowRequest(BaseModel):
    player: str = Field(description="Nom du joueur")
    force: float = Field(description="Force du lancer (0-1)", ge=0, le=1)
    angle_horizontal: float = Field(description="Angle horizontal en degrés")
    angle_vertical: float = Field(description="Angle vertical en degrés (0-90)")
    effect: float = Field(description="Effet latéral (-1 à 1)", ge=-1, le=1, default=0)

class GameState(BaseModel):
    balls: List[Ball]
    cochonnet: Optional[Ball]
    current_player: Optional[str]
    scores: Dict[str, int]
    game_phase: str

class GameSimulator:
    def __init__(self):
        self.balls: List[Ball] = []
        self.cochonnet: Optional[Ball] = None
        self.current_player: Optional[str] = None
        self.scores: Dict[str, int] = {}
        self.game_phase: str = "waiting"
        self.ball_counter: int = 0
        
        self.terrain_width = 4.0
        self.terrain_length = 15.0
        
    def reset_game(self):
        self.balls = []
        self.cochonnet = None
        self.current_player = None
        self.scores = {}
        self.game_phase = "waiting"
        self.ball_counter = 0
        
    def place_cochonnet(self, x: float, z: float):
        if not (1 <= z <= 12 and -self.terrain_width/2 <= x <= self.terrain_width/2):
            raise ValueError("Position du cochonnet hors limites")
            
        self.cochonnet = Ball(
            id="cochonnet",
            type=BallType.COCHONNET,
            position=(x, 0.03, z),
            color="white"
        )
        self.game_phase = "playing"
        
    def throw_ball(self, player: str, force: float, angle_h: float, angle_v: float, effect: float = 0):
        if not self.cochonnet:
            raise ValueError("Le cochonnet doit être placé avant de lancer")
            
        start_x = effect * 0.5
        start_y = 0.5
        start_z = -1.0
        
        angle_h_rad = np.radians(angle_h)
        angle_v_rad = np.radians(angle_v)
        
        velocity_magnitude = force * 6
        vx = velocity_magnitude * np.sin(angle_h_rad) + effect * 1
        vy = velocity_magnitude * np.sin(angle_v_rad)
        vz = velocity_magnitude * np.cos(angle_v_rad) * np.cos(angle_h_rad)
        
        ball = Ball(
            id=f"ball_{self.ball_counter}",
            type=BallType.BOULE,
            position=(start_x, start_y, start_z),
            velocity=(vx, vy, vz),
            player=player,
            color="red" if self.ball_counter % 2 == 0 else "blue"
        )
        
        self.balls.append(ball)
        self.ball_counter += 1
        
        asyncio.create_task(self.simulate_ball_physics(ball))
        
        return ball
        
    async def simulate_ball_physics(self, ball: Ball):
        dt = 0.05
        gravity = -9.81
        friction = 0.9
        restitution = 0.4
        
        pos = list(ball.position)
        vel = list(ball.velocity)
        
        for _ in range(200):
            vel[1] += gravity * dt
            
            pos[0] += vel[0] * dt
            pos[1] += vel[1] * dt
            pos[2] += vel[2] * dt
            
            if pos[1] <= 0.08:
                pos[1] = 0.08
                vel[1] = -vel[1] * restitution
                
                vel[0] *= (1 - friction * dt)
                vel[2] *= (1 - friction * dt)
            
            if abs(pos[0]) > self.terrain_width/2:
                pos[0] = np.sign(pos[0]) * self.terrain_width/2
                vel[0] = -vel[0] * 0.5
                
            if pos[2] > self.terrain_length - 0.5:
                pos[2] = self.terrain_length - 0.5
                vel[2] = -vel[2] * 0.3
                
            if pos[2] < -2:
                break
                
            ball.position = tuple(pos)
            ball.velocity = tuple(vel)
            
            if np.linalg.norm(vel) < 0.1:
                ball.velocity = (0, 0, 0)
                break
                
            await asyncio.sleep(dt)
            
    def get_distances(self) -> List[Dict]:
        if not self.cochonnet:
            return []
            
        distances = []
        cochonnet_pos = np.array(self.cochonnet.position)
        
        for ball in self.balls:
            ball_pos = np.array(ball.position)
            distance = np.linalg.norm(ball_pos - cochonnet_pos)
            distances.append({
                "ball_id": ball.id,
                "player": ball.player,
                "distance": float(distance)
            })
            
        return sorted(distances, key=lambda x: x["distance"])
        
    def get_state(self) -> GameState:
        return GameState(
            balls=self.balls,
            cochonnet=self.cochonnet,
            current_player=self.current_player,
            scores=self.scores,
            game_phase=self.game_phase
        )

simulator = GameSimulator()

@app.post("/reset")
async def reset_game():
    simulator.reset_game()
    return {"message": "Partie réinitialisée"}

@app.post("/cochonnet/place")
async def place_cochonnet(x: float, z: float):
    try:
        simulator.place_cochonnet(x, z)
        return {"message": "Cochonnet placé", "position": [x, 0.03, z]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ball/throw")
async def throw_ball(request: ThrowRequest):
    try:
        ball = simulator.throw_ball(
            request.player,
            request.force,
            request.angle_horizontal,
            request.angle_vertical,
            request.effect
        )
        return {"message": "Boule lancée", "ball_id": ball.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state")
async def get_game_state():
    return simulator.get_state()

@app.get("/distances")
async def get_distances():
    return {"distances": simulator.get_distances()}

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
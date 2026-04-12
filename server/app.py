from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Global state
state = {
    "step": 0,
    "done": False,
    "score": 0.0
}

# Action schema (IMPORTANT)
class Action(BaseModel):
    action_type: str
    value: Optional[str] = ""

@app.post("/reset")
def reset():
    state["step"] = 0
    state["done"] = False
    state["score"] = 0.0

    return {
        "observation": {
            "step": 0,
            "score": 0.0
        },
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/step")
def step(action: Action):
    state["step"] += 1

    # SAFE rewards (strictly between 0 and 1)
    if action.action_type == "answer" and action.value:
        reward = 0.8
    elif action.action_type == "hint":
        reward = 0.3
    elif action.action_type == "skip":
        reward = 0.1
    else:
        reward = 0.2

    state["score"] += reward

    done = state["step"] >= 4
    state["done"] = done

    return {
        "observation": {
            "step": state["step"],
            "score": state["score"]
        },
        "reward": float(round(reward, 2)),
        "done": done,
        "info": {}
    }

# 🔥 REQUIRED ENDPOINT
@app.get("/state")
def get_state():
    return {
        "step": state["step"],
        "score": state["score"],
        "done": state["done"]
    }

# Optional health check
@app.get("/health")
def health():
    return {"status": "ok"}

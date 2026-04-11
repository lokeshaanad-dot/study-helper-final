from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# State
state = {
    "step": 0,
    "done": False,
    "score": 0.0
}

# Action schema
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
        "reward": 0.5,   # must be between 0 and 1
        "done": False,
        "info": {}
    }

@app.post("/step")
def step(action: Action):
    state["step"] += 1

    # ✅ SAFE DEFAULT REWARD
    reward = 0.5

    # ✅ FIXED REWARD LOGIC (STRICTLY BETWEEN 0 AND 1)
    if action.action_type == "answer" and action.value:
        reward = 0.8
        state["score"] += reward
    elif action.action_type == "hint":
        reward = 0.4
    elif action.action_type == "skip":
        reward = 0.2

    done = state["step"] >= 3
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

@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

state = {
    "step": 0,
    "done": False,
    "score": 0.0
}

class Action(BaseModel):
    action_type: str
    value: Optional[str] = ""

@app.post("/reset")
def reset():
    state["step"] = 0
    state["done"] = False
    state["score"] = 0.0

    return {
        "observation": {"step": 0, "score": 0.0},
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/step")
def step(action: Action):
    state["step"] += 1

    reward = 0.0

    if action.action_type == "answer" and action.value:
        reward = 1.0
        state["score"] += reward
    elif action.action_type == "hint":
        reward = 0.2
    elif action.action_type == "skip":
        reward = -0.1

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


# 🔥 REQUIRED main() function
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


# 🔥 REQUIRED entry point
if __name__ == "__main__":
    main()
@app.get("/state")
def get_state():
    return {
        "step": state["step"],
        "score": state["score"],
        "done": state["done"]
    }

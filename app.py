from fastapi import FastAPI
import random

app = FastAPI()

state = {"step": 0}

@app.post("/reset")
def reset():
    state["step"] = 0
    return {
        "observation": {"step": 0},
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/step")
def step(action: dict):
    state["step"] += 1
    done = state["step"] >= 3

    return {
        "observation": {"step": state["step"]},
        "reward": 1.0 if done else 0.0,
        "done": done,
        "info": {}
    }

@app.get("/health")
def health():
    return {"status": "ok"}

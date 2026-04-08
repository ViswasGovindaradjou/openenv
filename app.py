from fastapi import FastAPI
from env import SupportEnv
from models import Action
from grader import grade
from tasks import TASKS
from baseline import run_baseline

app = FastAPI(
    title="OpenEnv SLA Support v3",
    docs_url="/docs",        # 👈 enable Swagger UI
    redoc_url="/redoc",      # 👈 optional
    openapi_url="/openapi.json",
    root_path=""             # 👈 important for HF Spaces
)

env = SupportEnv(seed=42, max_steps=15)

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    return env.step(action)

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def tasks():
    return {
        "tasks": TASKS,
        "action_schema": Action.schema()
    }

@app.get("/grader")
def grader(task_id: str):
    return {"score": grade(env.tickets, env.gt, task_id)}

@app.get("/baseline")
def baseline():
    return run_baseline()

@app.get("/")
def home():
    return {
        "message": "OpenEnv SLA Support Environment Running",
        "docs": "/docs"
    }
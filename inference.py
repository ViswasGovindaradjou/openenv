import os
import requests

# Required env variables (do not remove)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline")

def run():
    # Reset environment
    state = requests.post(f"{API_BASE_URL}/reset").json()

    tickets = state["tickets"]

    for t in tickets:
        text = t["text"].lower()

        # ---------- CLASSIFY ----------
        if "payment" in text or "refund" in text:
            category = "billing"
        elif "crash" in text:
            category = "technical"
        else:
            category = "general"

        requests.post(f"{API_BASE_URL}/step", json={
            "type": "classify",
            "ticket_id": t["id"],
            "value": category
        })

        # ---------- RESPOND ----------
        requests.post(f"{API_BASE_URL}/step", json={
            "type": "respond",
            "ticket_id": t["id"],
            "value": "We are working on your issue."
        })

        # ---------- ESCALATE ----------
        if t["sentiment"] == "angry":
            requests.post(f"{API_BASE_URL}/step", json={
                "type": "escalate",
                "ticket_id": t["id"],
                "value": "urgent"
            })

    # Get final score
    score = requests.get(f"{API_BASE_URL}/grader?task_id=hard").json()
    print("FINAL SCORE:", score)


if __name__ == "__main__":
    run()
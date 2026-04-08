import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")

def solve():
    # RESET ENV
    state = requests.post(f"{BASE_URL}/reset").json()

    tickets = state["tickets"]

    # HANDLE ALL TICKETS
    for t in tickets:
        text = t["text"].lower()
        sentiment = t["sentiment"]

        # ---------- CLASSIFY ----------
        if "payment" in text:
            category = "billing"
        elif "crash" in text:
            category = "technical"
        elif "refund" in text:
            category = "refund"
        else:
            category = "general"

        requests.post(f"{BASE_URL}/step", json={
            "type": "classify",
            "ticket_id": t["id"],
            "value": category
        })

        # ---------- RESPOND ----------
        requests.post(f"{BASE_URL}/step", json={
            "type": "respond",
            "ticket_id": t["id"]
        })

        # ---------- ESCALATE ----------
        if sentiment == "angry":
            requests.post(f"{BASE_URL}/step", json={
                "type": "escalate",
                "ticket_id": t["id"]
            })

    # GET FINAL SCORE
    result = requests.get(f"{BASE_URL}/grader", params={"task_id": "hard"}).json()

    return result


if __name__ == "__main__":
    print(solve())

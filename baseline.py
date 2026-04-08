from env import SupportEnv
from models import Action
from grader import grade

def run_baseline():
    env = SupportEnv(seed=42, max_steps=15)
    obs = env.reset()
    done = False

    while not done:
        for t in obs.tickets:
            text = t.text.lower()

            # ---------- BETTER CLASSIFICATION ----------
            if "payment" in text:
                cat = "billing"
            elif "crash" in text or "error" in text:
                cat = "technical"
            elif "refund" in text:
                cat = "refund"
            else:
                cat = "general"

            obs, _, done, _ = env.step(Action(type="classify", ticket_id=t.id, value=cat))
            if done: break

            # ---------- ALWAYS RESPOND ----------
            obs, _, done, _ = env.step(Action(type="respond", ticket_id=t.id))
            if done: break

            # ---------- ESCALATE ONLY WHEN ANGRY ----------
            if t.sentiment == "angry":
                obs, _, done, _ = env.step(Action(type="escalate", ticket_id=t.id))
            if done: break

    return {
        "easy": grade(env.tickets, env.gt, "easy"),
        "medium": grade(env.tickets, env.gt, "medium"),
        "hard": grade(env.tickets, env.gt, "hard"),
    }
